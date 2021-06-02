<template>
    <div id="graph">
      <div id="container"></div>
    </div>
</template>

<script>
import * as Three from 'three';
import * as echarts from 'echarts';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { Lut } from 'three/examples/jsm/math/Lut.js';
import CSG from '../util/three-csg.js';

export default {
  name: 'ThreeTest',
  data() {
    return {
      container: null,
      camera: null,
      scene: null,
      orthoCamera: null,
      ui_scene: null,
      renderer: null,
      mesh: null,
      controls: null,
      know_vars: {},
      meshResult: null,
      mode: '',
      xData: [],
      yData: [],
      r_data: [
     [
        echarts.number.round(3.8),
        echarts.number.round(4)
     ],
     [
        echarts.number.round(3.8),
        echarts.number.round(4.5)
     ],
     [
        echarts.number.round(5),
        echarts.number.round(6)
     ]],

    }
  },
  methods: {
    parseGeoJson: function(json) {
      var jsonObj = JSON.parse('{ "id": "result", "content": null, "children": [ { "id": "BitAnd", "content": null, "children": [ { "id": "e", "content": null, "children": [ { "id": "BitAnd", "content": null, "children": [ { "id": "e1", "content": { "params": [ [ 0, 0 ], [ 1, 1 ] ], "type": "Rectangle" }, "children": [] }, { "id": "e2", "content": { "params": [ [ 0, 0 ], 1 ], "type": "Disk" }, "children": [] } ] } ] }, { "id": "e1", "content": { "params": [ [ 0, 0 ], [ 1, 1 ] ], "type": "Rectangle" }, "children": []}]}]}');
      // var jsonObj = JSON.parse(json)
      var result_id = jsonObj.id;
      this.mode = "2d"
      // this.mode = jsonObj.mode;
      this.traverse(jsonObj);
      let bspResult = this.know_vars[result_id];
      this.meshResult = CSG.toMesh(bspResult, new Three.Matrix4());
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


    init: function(jsonObj) {
      this.parseGeoJson(jsonObj);
      if(this.mode=="2d") {
        this.initEcharts();
      }
      else if(this.mode == "3d") {
        return
      }
    },

    initEcharts: function() {
      this.charts = echarts.init(document.getElementById("container"));
      var option = {
          xAxis: {},
          yAxis: {},
          series: [
              {
                  type: 'custom',
                  renderItem: this.renderItem,
                  data: this.r_data
              }
          ]
      };
      this.charts.setOption(option);
    },

    renderItem: function(params, api) {
        if (params.context.rendered) {
            return;
        }

        params.context.rendered = true;

        let points = [];
        for (let i = 0; i < this.r_data.length; i++) {
            points.push(api.coord(this.r_data[i]));
        }

        let color = api.visual('color');

        return {
            type: 'polygon',
            shape: {
                points: echarts.graphic.clipPointsByRect(points, {
                    x: params.coordSys.x,
                    y: params.coordSys.y,
                    width: params.coordSys.width,
                    height: params.coordSys.height
                })
            },
            style: api.style({
                fill: color,
                stroke: echarts.color.lift(color)
            })
        };
    },



    old_init: function() {
        this.container = document.getElementById('container');


        // 1.建立相机 和 场景，包括了主视图还有UI
        this.camera = new Three.PerspectiveCamera(70, this.container.clientWidth/this.container.clientHeight, 1, 100);
        this.camera.position.set( 5, 5, 5 );
        const pointLight = new Three.PointLight( 0xffffff, 1 );
				this.camera.add( pointLight );

        this.orthoCamera = new Three.OrthographicCamera( - 1, 1, 1, - 1, 1, 2 );
				this.orthoCamera.position.set( 0.5, 0, 1 );

        this.scene = new Three.Scene();
        this.scene.background = new Three.Color( 0xffffff );
        this.scene.add(this.camera);

        this.ui_scene = new Three.Scene();



        let lut = new Lut();
        let sprite = new Three.Sprite( new Three.SpriteMaterial( {
					map: new Three.CanvasTexture( lut.createCanvas() )
				} ) );
				sprite.scale.x = 0.125;
				this.ui_scene.add( sprite );



        this.parseGeoJson();
        let material = new Three.MeshNormalMaterial();
        this.meshResult.material = material;
        this.scene.add(this.meshResult);
        

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
        this.container.appendChild(this.renderer.domElement);
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);

        // window.addEventListener( 'resize', onWindowResize );

				this.controls = new OrbitControls( this.camera, this.renderer.domElement );
				// controls.addEventListener( 'change', render );

        // this.scene.add(new THREE.GridHelper(50, 25, 0x000040, 0x000040));

    },
    animate: function() {
        requestAnimationFrame(this.animate);
        // this.mesh.rotation.x += 0.01;
        // this.mesh.rotation.y += 0.02;
        this.controls.update();
        this.renderer.clear();
        this.renderer.render(this.scene, this.camera);
        // this.renderer.render(this.ui_scene, this.orthoCamera );
    },
    onWindowResize: function() {
      this.camera.aspect = this.container.clientWidth/this.container.clientHeight;
			this.camera.updateProjectionMatrix();
      this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    }
  },
  mounted() {
      this.initEcharts();
      // this.animate();
  }
}
</script>

<style scoped>
#graph {
  width: 70%;
  height: 100%;
}
#container {
  width: 100%;
  height: 60%;
  background-color: rgb(243, 224, 224);
  display: flex;
}
</style>