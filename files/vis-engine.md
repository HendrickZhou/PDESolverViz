# 可视化引擎的的进一步调研

## 需求
我们渴望的效果是，引擎能够对2d和3d进行类似COMSOL那种CAD风格的渲染。  

对于2d的情况，可以描述为有形状cad风格的二维热力图heatmap，支持缩放以及其他基础plot的效果。  
对于3d的情况，即具有切片效果/时序动画效果的3d几何体可视化。

## 2d/3d引擎选择
[web js可视化库合集](https://gist.github.com/dmnsgn/76878ba6903cf15789b712464875cfdc)
1. three.js  
[3d NLP模型的可视化](https://medium.com/cortico/3d-data-visualization-with-react-and-three-js-7272fb6de432)  
[3d热力图的切片操作](http://www.uwenku.com/question/p-odadfspz-xp.html)  
[three.j几何体的描述](https://cloud.tencent.com/developer/article/1689738?from=information.detail.three.js%E5%A4%9A%E8%BE%B9%E5%BD%A2%E5%B1%9E%E6%80%A7)  
[three.js 2d散点图可视化](https://blog.fastforwardlabs.com/2017/10/04/first-look-using-three.js-for-2d-data-visualization.html)
[three.js heatmap](https://www.programmersought.com/article/8593787256/)  
[three.js 热力图](https://blog.csdn.net/weixin_42443851/article/details/101374410)  
[设置2d的视图](https://stackoverflow.com/questions/21786184/setting-up-a-2d-view-in-three-js)
学习成本高，2d的可视化要造的轮子太多

2. 直接用webGL开发  
[webGL 2d绘图](https://cloud.tencent.com/developer/article/1006110?from=information.detail.three.js%E5%A4%9A%E8%BE%B9%E5%BD%A2%E5%B1%9E%E6%80%A7)   
[webGL 2d，官方](https://developer.mozilla.org/zh-CN/docs/Web/API/WebGL_API/Tutorial/Adding_2D_content_to_a_WebGL_context)  
[webGL heatmap轮子](https://github.com/pyalot/webgl-heatmap/blob/master/webgl-heatmap.js)  
要造的轮子太多了，坐标轴等基础的东西都要重新造，时间不够。  

3. OpenJSCad  
[github repository](https://github.com/jscad/OpenJSCAD.org)  
[csg.js一个几何体模型操作库](https://github.com/evanw/csg.js/blob/master/csg.js)  
转译cad实在是太太太方便了，风格也是很理想，但是2d的渲染效果未知。但是好像是基于openGL开发的，如果要重造轮子，可能会面临超大的工作量；  
不知道热力图渲染效果！不知道怎么把图形转化为equation!

4. VTK.js & xtk.js  
[xtk.js](https://github.com/xtk/X)

5. echarts  


6. two.js  


## 其他
1. svg vs canvas  
[svg&canvas](https://zhuanlan.zhihu.com/p/190134690)




## 困难
1. 绘图风格的统一，如果使用不同的框架可能会发生差异；绘图原理的区分：2d可能更适合基于canvas的渲染方法，而3d更适合webGL的渲染方法。

2. 2d引擎对于带有几何体形状的热力图的支持

3. 框架能够方便对几何体形式描述的转译  

4. 能够快速实时渲染热力值