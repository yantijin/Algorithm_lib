### 算法流程
* 随机采样，确定采样数据集大小s
* 采用PAA对于时间序列进行降维处理
	* 设置d，根据typical frequency计算，typical frequency为根据自相关函数的第一个极小点对应的lag的倒数
	* 将typical frequency按照降序排序，选择一个80%位置对应的typical frequency作为上限
* 对于采样数据集进行聚类处理：DBSCAN
	* 设置radius的候选列表，根据斜率进行计算求解吧，然后对于不同的radius依次执行DBSCAN算法
* 分配算法：
	* 在DBSCAN中，如果一个对象是核心对象，那么把他存储到SNG中，然后执行assignment算法

### 参数设置
* 采样数据集大小s的确定：
	* 下界：
		* m=5
		* $\alpha = 0.05$
	* 上界
		* $\alpha = 0.05$
		* $\epsilon = 0.01$
	* 函数 calSampleSize(m, $\alpha$, $\epsilon$)
		* 返回 上下界两个参数

* PAA降维计算:
	* 确定分多少段(d)
	* 对采样数据集中每一段执行PAA
	* 函数 PAA(TS, d)
		* 返回 降维之后的TS

	* 计算typicalFrequency
		* calTypicalFrequency(TS)
		* 计算自相关函数并返回第一个极小值  calAutoCorrelation(TS)
		* 对返回极小值取倒数并按照降序排列
		* 返回  列表 typicalFrequency
	* 确定PAA参数d
		* 调用caltypicalFrequency(TS)
		* 对得到的typicalFrequency取80%对应的值，然后两倍频率，然后**计算d**

* DBSCAN中 
	* 参数设置
		* k = 4
		* radius列表  DensityRadius(data, k)
			* calKdis(data, k)  返回$k_dis$列表、
			* 然后计算左侧和右侧斜率差别是否在一定的范围之内，然后找到第一个点，然后分为两部分，迭代进行此搜索
	* 对于radius列表中的radius依次进行DBSCAN聚类、
		* 返回： 类别(类型为map)，核心对象列表coreObjects


* Assignment
	* Assignment(data, coreObjects)
