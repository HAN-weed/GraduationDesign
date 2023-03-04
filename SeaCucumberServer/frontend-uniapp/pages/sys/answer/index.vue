<template>
	<view class="content" >
		<js-lang title="answer.title"></js-lang>
		<view class="cul-wrapper">
			<view v-if="isOver" class="msg-over">没有更多消息了</view>
			<block v-for="(item,index) in hisMsgs" :key="item.id">
				<view :class="[item.isme?'msg-me':'msg-service']" :id="item.id">
					<view class="msg-text">
						<view class="msg-text-content">
							<text>{{item.msg}}</text>
						</view>
					</view>
				</view>
			</block>
			<view class="cul-date">{{curDate | formatDate}}</view>
			<block>
				<view class="msg-service">
					<view class="msg-text">
						<view class="msg-text-content">
							<text>您好，小助手将为您解答</text>
							<!-- <view class="msg-introduce">您好，我将为您解答。</view>
							<view class="msg-classify">
								<view class="msg-classify-tit"><text class="msg-classify-name">分类1：</text>分类描述分类描述分类描述分类描述分类描述分类描述。</view>
								<view class="msg-classify-click" @click="consultClick(1)">[此类问题请点我]</view>
							</view>
							<view class="msg-introduce">您好，请先选择问题分类，我将为您解答。</view>
							<view class="msg-classify">
								<view class="msg-classify-tit"><text class="msg-classify-name">分类2：</text>分类描述分类描述分类描述分类描述分类描述分类描述。</view>
								<view class="msg-classify-click" @click="consultClick(2)">[此类问题请点我]</view>
							</view>
							<view class="msg-introduce">您好，请先选择问题分类，我将为您解答。</view>
							<view class="msg-classify">
								<view class="msg-classify-tit"><text class="msg-classify-name">分类3：</text>分类描述分类描述分类描述分类描述分类描述分类描述。</view>
								<view class="msg-classify-click" @click="consultClick(3)">[此类问题请点我]</view>
							</view> -->
						</view>
					</view>
				</view>
			</block>
			<block v-for="(item,index) in msgs" :key="index">
				<view :class="[item.isme?'msg-me':'msg-service']" :id="'msg-'+index">
					<view class="msg-text">
						<view class="msg-text-content">
							<text>{{item.msg}}</text>
						</view>
					</view>
				</view>
			</block>
		</view>
		<view class="operation" :class="{'conversion':!conversion}">
			<input class="uni-input" type="text" v-model="msgInput.msg1" :class="[conversion?'msg-input1':'msg-input2']" @tap="sub1(msgInput.msg2)" />
			<input type="text" v-model="msgInput.msg2" :class="[conversion?'msg-input2':'msg-input1']" @tap="sub2(msgInput.msg1)" />
		</view>
	</view>
</template>
<script>
/**
 * Copyright (c) 2013-Now http://jeesite.com All rights reserved.
 */
export default {
		data() {
			return {
				indexRegion:'',
				listPage: 0,
				isOver: false,
				curDate: '1588061853944',
				//控制按钮和文本框样式和功能的转换
				conversion: true,
				msgInput: {
					msg1: '',
					msg2: ''
				},
				//消息列表
				msgs: [],
				hisMsgs: []
			}
		},
		onLoad(e) {
		   this.indexRegion = uni.getStorageSync('indexReg');
		   console.log(this.indexRegion)
		  }, 
		filters: {
			formatDate: function(value) {
				var date = new Date();
				//date.setTime(value);
				var month = date.getMonth() + 1;
				var hours = date.getHours();
				if (hours < 10)
					hours = "0" + hours;
				var minutes = date.getMinutes();
				if (minutes < 10)
					minutes = "0" + minutes;
				var time = date.getFullYear() + "-" + month + "-" + date.getDate() +
					" " + hours + ":" + minutes;
				return time;
			}

		},
		onBackPress() {
		     uni.setStorageSync('setStatusIndexFunc', 0);
		     // this.active = 0;
		     uni.navigateTo({
		      url: '../index/index?region='+this.indexRegion
		     });
		     return true
		    },  
		methods: {
			endOver() { //设置禁用下拉加载
				const pages = getCurrentPages();
				const page = pages[pages.length - 1];
				const currentWebview = page.$getAppWebview();
				currentWebview.setStyle({
					pullToRefresh: {
						support: false,
						style: plus.os.name === 'Android' ? 'circle' : 'default'
					}
				});
				console.log('没有更多数据了，禁用');
			},
			consultClick(id) {
				console.log(id)
				this.sub(id)
			},
			//滚动到指定位置
			jumpScroll() {
				this.$nextTick(function() {
					uni.pageScrollTo({
						scrollTop: 99999,
						duration: 0
					});
				})
			},
			sendMsg(obj) {
				let anotherMsg = {
					isme: false,
					msg: obj
				}
				this.msgs.push(anotherMsg)
				this.jumpScroll()
			},
			sub1(val) {
				if (!this.conversion) {
					this.sub(val)
				}
			},
			sub2(val) {
				if (this.conversion) {
					this.sub(val)
				}
			},
			sub(val) {
				console.log('222')
				console.log(val)
				let _self = this;
				if (val) {
					//清空输入框中的文字
					this.msgInput.msg1 = ''
					this.msgInput.msg2 = ''
					
					let msg = {
						isme: true,
						msg: val
					}
					this.msgs.push(msg)
					this.conversion = !this.conversion
					this.jumpScroll()
					this.$u.api.kbqa({
						question : val
					}).then(res=>{
						this.sendMsg(res)
					})
				} else {
					this.conversion = !this.conversion
					this.jumpScroll()
				}
			}
		},
		onPullDownRefresh() {
			let _this = this;
			console.log('refresh2');
			let msgArr = [{
					msg: '问题1',
					id: 'm1',
					mark: 'me',
					isme: true,
					time: '2020-10-1'
				},
				{
					msg: '回复1',
					id: 'l1',
					mark: 'service',
					isme: false,
					time: '2020-10-2'
				},
				{
					msg: '问题2',
					id: 'm2',
					mark: 'me',
					isme: true,
					time: '2020-10-1'
				},
				{
					msg: '回复2',
					id: 'l2',
					mark: 'service',
					isme: false,
					time: '2020-10-2'
				}
			]

			this.hisMsgs.push(...msgArr)
			console.log('this.hisMsgs1')
			console.log(this.hisMsgs)
			setTimeout(function() {
				uni.stopPullDownRefresh();
			}, 100);
		},
	}
</script>
<style lang="scss">
page {
	background-color: #f8f8f8;
}
	.content {
		display: flex;
		flex-direction: column;
		align-items: center;
		flex: 1;
		
	}
	
	.msg-over {
		font-size: 24rpx;
		text-align: center;
		color: #999999;
	}

	.cul-wrapper {
		padding: 0 35rpx;
		box-sizing: border-box;
		padding-bottom:175rpx;
	}

	.cul-date {
		padding-top: 20rpx;
		color: #999999;
		font-size: 24rpx;
		text-align: center;
	}

	.msg-me,
	.msg-service {
		display: flex;
		align-items: flex-start;
		width: 680rpx;
		margin: 30rpx 0;
		box-sizing: border-box;
		overflow: hidden;
	}

	/* .bg{
			background-color: blue;
		} */
	.msg-me {
		justify-content: flex-end;
	}

	.msg-service {
		justify-content: flex-start;
	}

	.avatar {
		width: 70rpx;
		height: 70rpx;
		border-radius: 50%;
	}

	.msg-text {
		width: 560rpx;
	}

	.msg-me>.msg-text {
		display: flex;
		justify-content: flex-end;
	}

	.msg-text-content {
		line-height: 35rpx;
		display: inline-block;
		box-sizing: border-box;
		padding: 30rpx;
		font-size: 28rpx;
	}

	.msg-introduce {
		color: #333333;
		font-size: 26rpx;
		line-height: 36rpx;
	}

	.msg-classify-tit {
		color: #333333;
		font-size: 26rpx;
		line-height: 43rpx;
	}

	.msg-classify-name {
		font-size: 30rpx;
		font-weight: bold;
	}

	.msg-classify-click {
		color: #2B8FFF;
		font-size: 26rpx;
		line-height: 56rpx;
	}

	.msg-me>.msg-text>.msg-text-content {
		margin-left: 70rpx;
		background-color: #2B8FFF;
		color: #FFFFFF;
		font-size: 30rpx;
		border-top-right-radius: 44rpx;
		border-bottom-left-radius: 44rpx;
		border-top-left-radius: 44rpx;
		margin-right: 15rpx;
	}

	.msg-service>.msg-text>.msg-text-content {
		color: #333333;
		margin-left: 15rpx;
		background-color: #FFFFFF;
		/* border: 1rpx solid #d5e0e5; */
		border-bottom-left-radius: 44rpx;
		border-bottom-right-radius: 44rpx;
		border-top-right-radius: 44rpx;
		/* 		margin-right: 70rpx; */
		color: #333333;
	}

	.operation {
		display: flex;
		position: fixed;
		left: 0;
		bottom: 130rpx;
		align-items: center;
		/* background-color: transparent; */
		background: #ffffff;
		/* padding: 10px 35rpx; */
		border-top: 1rpx solid rgba(184, 184, 184, 0.1);
		width: 100vw;
	}

	.conversion {
		flex-direction: row-reverse;
		justify-content: flex-end;
	}

	.msg-input1 {
		background: #FFFFFF;
		height: 30px;
		width: 600rpx;
		border-radius: 10px;
		padding: 0 20rpx;
		border: 1rpx solid rgba(0, 0, 0, 0.1);
	}

	.msg-input2 {
		display: flex;
		align-items: center;
		width: 100rpx;
		height: 40px;
		background-image: url('data:image/png;base64,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');
		background-repeat: no-repeat;
		background-position: center center;
		background-size: 47rpx 42rpx;
		/*这个颜色是因为组件位置交换的时候，字体会有一瞬间继续留在框内，这里把内容变为透明即可*/
		color: rgba(0, 0, 0, 0);
	}
</style>
