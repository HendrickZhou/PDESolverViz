# PDESolverViz
Visulization of PDE's Deep learning Solution

## 技术选型
### 可视化端
1. JS可视化库调研：
* 通用科学绘图：  
G2/F2 蚂蚁
Echarts 百度
fusioncharts
D3.js  
Echarts的可定制性比不上D3.js
* 3D:  
Three.js, evercraft
在展示3d的方程解空间的时候可能会用上

2. 场景  
科学可视化UI，可视化方程  - Echarts  
神经网络训练UI - D3.js  
计算域UI，边值设计  -  ？？？

### 前端
1. React.js, vue.js  
可以认为是主打前端的框架，是一个js的库  
react的核心是virutal DOM(组件化) + JSX  
vue是响应式的框架,如其名，强势在view的处理这一块
2. Angular.js  
一个client-side MV*框架,适合处理大型项目，学习成本高
3. Node.js  
Node其实算在后端里，因为是server-side框架，自带一个v8引擎。其作用和java后端很像

前端可以优先选择使用vue.js，学习曲线比较好，轻量化。

### 后端
使用Python-based框架，因为后台的计算使用PyTorch/Tensorlflow框架，这样可以保持最大的兼容性和学习成本  
候选的对象有Flask,Django,Tornado, Twisted. 前期会优先选择Flask。  
因为Django更适合典型的web的复杂平台，和我们的需求可能不太一致。所以会放弃。 
而Tornado和Twisted会更快速一点，但是有学习成本，后期优化的时候再考虑。 

Nodejs也是一个很好的选择，不过js在处理科学计算接口的时候应该会超级麻烦


redis是用缓存手段解决数据库高并发场景，而kafka是类似消息队列方式解耦两个系统的消息（有点像ros），目前看来不需要用这两项技术，除非碰到性能瓶颈。

## 优化预期
1. 神经网络训练UI  
后端在训练时可能要实现实时和前端通讯
2. 科学可视化UI  


## 参考构架 - TFMeter项目
typescript + d3.js，除此之外就没有使用任何框架，因为dl算法部分是用ts手写的，也没有用到后端服务器