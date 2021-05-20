<template>
    <div id="graph">
      <div id="container"></div>
    </div>
</template>

<script>
import * as Three from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import CSG from '../util/three-csg.js';

export default {
  name: 'ThreeTest',
  data() {
    return {
      camera: null,
      scene: null,
      renderer: null,
      mesh: null,
      control: null,
      know_vars: {},
    }
  },
  methods: {
    createHeightMap(){
      var canvas = document.createElement("canvas");
      canvas.width = 256;
      canvas.height = 256;
      var ctx = canvas.getContext("2d");
      ctx.fillStyle = "black";
      ctx.fillRect(0, 0, 256, 256);
      for(let i = 0; i < 100; i++){
        var x = Math.floor(Math.random() * 255);
          var y = Math.floor(Math.random() * 255);
          var radius = 50;
          var grd = ctx.createRadialGradient(x, y, 1, x, y, radius);
          var h8 = Math.floor(Math.random() * 255);
          grd.addColorStop(0, "rgb("+ h8 + "," + h8 + "," + h8 +")");
          grd.addColorStop(1, "transparent");
          ctx.fillStyle = grd;
          ctx.fillRect(0, 0, 256, 256);
      }
      return new Three.CanvasTexture(canvas);
    },
    parseGeoJson: function() {
      var jsonObj = JSON.parse('{"id": "result", "content": null, "children": [{"id": "Add", "content": null, "children": [{"id": "e", "content": null, "children": [{"id": "Add", "content": null, "children": [{"id": "e1", "content": {"params": [[0, 0], [0.5, 0.5]], "type": "Rectangle"}, "children": []}, {"id": "e2", "content": {"params": [[0, 0], 3], "type": "Disk"}, "children": []}]}]}, {"id": "e1", "content": {"params": [[0, 0], [1, 1]], "type": "Rectangle"}, "children": []}]}]}');
      var result_id = jsonObj.id;
      this.traverse(jsonObj);
      let bspResult = this.know_vars[result_id];
      let meshResult = CSG.toMesh(bspResult, new Three.Matrix4());
      return meshResult;
    },
    traverse: function(treeObj) {
      if( treeObj.children[0] != null && typeof treeObj == "object" ) {
        var lhs = treeObj.id;
        var ops = treeObj.children[0];
        var left = treeObj.children[0].children[0];
        var right = treeObj.children[0].children[1];
        this.traverse(left);
        this.traverse(right);

        this.buildGeo(lhs, ops, left, right)
        console.log("build done");
      }
      else{
        return null
      }
    },

    geoXdeToThree: function(content) {
      if(content.type == "Rectangle") {
        let lb = content.params[0];
        let rt = content.params[1];
        let init_mesh_obj = new Three.Mesh(new Three.PlaneGeometry(rt[0]-lb[0], rt[1]-lb[1]));
        // init_mesh_obj = init_mesh_obj.add(new Three.Vector)
        return init_mesh_obj;
      } else if(content.type == "Disk") {
        let center = content.params[0];
        let radius = content.params[1];
        console.log(radius);
        let init_mesh_obj = new Three.Mesh(new Three.CircleGeometry(radius, 32));
        return init_mesh_obj;
      } else {
        return null;
      }
    },

    buildGeo: function(lhs_id, ops, left, right){
      // if left or right is first time difinition
      if(!(left.id in this.know_vars)) {
        let tmp_mesh_obj = this.geoXdeToThree(left.content)
        this.know_vars[left.id] = CSG.fromMesh(tmp_mesh_obj);
      }
      if(!(right.id in this.know_vars)) {
        let tmp_mesh_obj = this.geoXdeToThree(right.content)
        this.know_vars[right.id] = CSG.fromMesh(tmp_mesh_obj);
      }

      console.log(this.know_vars[left.id]);
      console.log(left.id);
      console.log(this.know_vars[right.id]);
      console.log(right.id);

      console.log(ops.id);
      // mesh obj ganranteed, work on bsp object
      if(ops.id == 'BitAnd') {
        this.know_vars[lhs_id] = this.know_vars[left.id].union(this.know_vars[right.id]);
        console.log(this.know_vars[lhs_id]);
      } else if(ops.id == 'Sub') {
        this.know_vars[lhs_id] = this.know_vars[left.id].subtract(this.know_vars[right.id]);
      } else if(ops.id == 'Add') {
        this.know_vars[lhs_id] = this.know_vars[left.id].intersect(this.know_vars[right.id]);
      } else {
        return null;
      }
    },
    init: function() {
        let container = document.getElementById('container');

        this.camera = new Three.PerspectiveCamera(70, container.clientWidth/container.clientHeight, 0.01, 10);
        this.camera.position.z = 1;

        this.scene = new Three.Scene();

        let geometry = new Three.BoxGeometry(5, 1, 1);
        // let meshA = new Three.Mesh(new Three.BoxGeometry(0.5,0.5,0.5));
        // let meshB = new Three.Mesh(new Three.BoxGeometry(0.5,0.5,0.5));
        // meshB.position.add(new Three.Vector3( 0.25, 0.25, 0.25));
        // meshA.updateMatrix();
        // meshB.updateMatrix();
        // let bspA = CSG.fromMesh( meshA );                        
        // let bspB = CSG.fromMesh( meshB );
        // let bspResult = bspA.subtract(bspB);
        // let meshResult = CSG.toMesh( bspResult, meshA.matrix, meshA.material )
        let meshResult = this.parseGeoJson();
        let material = new Three.MeshNormalMaterial();
        meshResult.material = material;
        // this.mesh = meshResult;
        this.mesh = new Three.Mesh(geometry, material);
        // this.scene.add(this.mesh);
        const size = 10;

        const divisions = 10;
        const gridHelper = new Three.GridHelper( size, divisions );
        this.scene.add( gridHelper );
        const axesHelper = new Three.AxesHelper( 5 );
        this.scene.add(axesHelper);

        // this.mesh.geometry.computeBoundingBox();
        // const box = new Three.Box3().setFromObject( this.mesh );
        // const bb = new Three.Box3Helper(box, 0xffff00);

        // this.scene.add(bb);
        // this.scene.add(this.mesh)


        this.renderer = new Three.WebGLRenderer({antialias: true});
        this.renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(this.renderer.domElement);

        // window.addEventListener( 'resize', onWindowResize );

				this.controls = new OrbitControls( this.camera, this.renderer.domElement );
				// controls.addEventListener( 'change', render );

        // this.scene.add(new THREE.GridHelper(50, 25, 0x000040, 0x000040));


        var heatVertex = `
          uniform sampler2D heightMap;
          uniform float heightRatio;
          varying vec2 vUv;
          varying float hValue;
          void main() {
            vUv = uv;
            vec3 pos = position;
            hValue = texture2D(heightMap, vUv).r;
            pos.y = hValue * heightRatio;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(pos,1.0);
          }
        `;
        
        var heatFragment = `
          varying float hValue;
          vec3 heatmapGradient(float t) {
            return clamp((pow(t, 1.5) * 0.8 + 0.2) * vec3(smoothstep(0.0, 0.35, t) + t * 0.5, smoothstep(0.5, 1.0, t), max(1.0 - t * 1.7, t * 7.0 - 6.0)), 0.0, 1.0);
          }

          void main() {
            float v = abs(hValue - 1.);
            gl_FragColor = vec4(heatmapGradient(hValue), 1. - v * v) ;
          }
        `;
        var heightMap = this.createHeightMap();
        var planeGeometry = new Three.PlaneBufferGeometry(50, 50, 1000, 1000);
        planeGeometry.rotateX(-Math.PI * 0.5);
        var heat = new Three.Mesh(planeGeometry, new Three.ShaderMaterial({
          uniforms: {
            heightMap: {value: heightMap},
            heightRatio: {value: 10}
          },
          vertexShader: heatVertex,
          fragmentShader: heatFragment,
          transparent: true
        }));

        this.scene.add(heat);

    },
    animate: function() {
        requestAnimationFrame(this.animate);
        // this.mesh.rotation.x += 0.01;
        // this.mesh.rotation.y += 0.02;
        this.controls.update();
        this.renderer.render(this.scene, this.camera);
    }
  },
  mounted() {
      this.init();
      this.animate();
  }
}
</script>

<style scoped>
#graph {
  width: 50%;
  height: 100%;
}
#container {
  width: 100%;
  height: 75%;
  background-color: rgb(243, 224, 224);
  display: flex;
}
</style>