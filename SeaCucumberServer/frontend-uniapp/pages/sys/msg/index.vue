<template>
	<view class="wrap">
		<js-lang title="recommend.title"></js-lang>
		<view class="search">
			<u-search v-model="keywords" @custom="search" @search="search"></u-search>
		</view>
		<scroll-view class="scroll-list" scroll-y="true">
			<u-collapse class="box" :accordion="false" :arrow="false">
				<view class="item" v-for="(item, index) in list" :key="item.code">
					<u-collapse-item :open="true">
						<view class="title" slot="title">
							<u-icon :name="item.icon != '' ? item.icon : 'home'" :size="35"></u-icon>
							<view class="text">{{item.name}}</view>
							<u-badge v-if="item.count && item.count > 0" :count="item.count"></u-badge>
						</view>
						<u-cell-group class="list" :border="false">
							<u-cell-item :arrow="true" v-for="(child, index2) in item.childList" :key="child.code" @click="navTo(child)">
								<text slot="title">{{child.name}}</text>
								<text slot="label">发送者：{{child.createByName}} | 时间：{{child.createDate}}</text>
							</u-cell-item>
						</u-cell-group>
					</u-collapse-item>
				</view>
			</u-collapse>
		</scroll-view>
	</view>
</template>
<script>
/**
 * Copyright (c) 2013-Now http://jeesite.com All rights reserved.
 */
export default {
	data() {
		
		return {
			userId : '',
			keywords: '',
			list: [],	
		};
	},
	onLoad() {
		this.getRecommend();
	},
	onPullDownRefresh() {
		this.getRecommend();
		setTimeout(function () {
			uni.stopPullDownRefresh();
		}, 1000);
	},
	methods: {
		navTo(child) {
			//防止在url中出现%而产生错误
			let itemData = JSON.stringify(child)
			let newitem = itemData.replace(/%/g,'%25');
			uni.navigateTo({
				url: '/pages/sys/msg/form?item='+ encodeURIComponent(newitem),
			});
		},
		search(value) {
			this.$u.toast('搜索内容为：' + value)
		},
		//从后台获取推荐的文章数据
		getRecommend(){
			const that = this
			var reslist = [];
			that.userId = getApp().globalData.userId
			this.$u.api.recommend({
				userId : that.userId
			}).then(res=>{
				res.forEach((item,index)=>{
					reslist[index] = {
						code: res[index]['articleId'],
						name: res[index]['tagName'],
						icon: 'chat',
						childList:[
							{
								code: res[index]['articleId'],
								name: res[index]['articleName'],
								content: res[index]['articleContent'],
								createByName: '管理员',
								createDate: '2021-4-6 12:10'
							}
						]
					}
				});
				that.list = reslist
				console.log(this.list)
			})
		}
	}
};
</script>
<style lang="scss">
page {
	background-color: #f8f8f8;
}
</style>
