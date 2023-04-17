<template>
	<view class="wrap">
		<view class="article-title">{{banner.title}}</view>
		<view class="article-meta">
			{{banner.author_name}} 发起于 {{banner.published_at}}</text>
		</view>
		<view class="article-content">
			<rich-text class=".rich-val" :nodes="content" space="emsp"></rich-text>
		</view>
		<view class="u-p-t-5"></view>
	</view>
</template>
<script>
/**
 * Copyright (c) 2013-Now http://jeesite.com All rights reserved.
 */
export default {
	data() {
		return {
			banner: {
				cover: '/static/jeesite/banner/2.svg',
				title: '刺参有病毒性疾病吗？感染的个体有何症状？',
				author_name: '系统管理员',
				published_at: '2021-4-20 12:30'
			},

		};
	},
	onLoad : function(option) {
		const that = this
		const item = JSON.parse(decodeURIComponent(option.item));
		console.log(item)
		this.content = item['content'].replace(/[\n]/gi,'<br />\xa0\xa0\xa0\xa0')
		
		this.banner['title'] = item['name']
		console.log(this.content)
		
	},
	methods: {
		navTo(url) {
			uni.navigateTo({
				url: url
			});
		}
	}
};
</script>
<style lang="scss">
page {
	background-color: #f8f8f8;
}
.article-title {
	font-size: 38rpx;
	font-weight: 400;
	text-align: center;
	padding-bottom: 30rpx;
	margin: 30rpx;
	border-bottom: 1px solid #c0c4cb;
	color: #51a0d5;
}
.article-meta {
	padding: 10rpx 50upx 30rpx;
	color: gray;
}
.article-content {
	padding: 0 30upx;
	overflow: hidden;
	font-size: 30rpx;
	line-height: 50rpx;
	margin-bottom: 30rpx;
	text-indent: 60rpx;
	/deep/ p {
		margin-bottom: 20rpx;
	}
}
.rich-val{
	word-break: break-all;
	white-space: pre-line;
	text-indent:2em;
}
</style>
