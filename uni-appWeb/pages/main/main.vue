<template>
    <view class="content">
		<uni-nav-bar :fixed="true" background-color="#20a0ff" :border="false">
			<view class="input-view"  v-if="current === 0">
				<uni-icons type="search" size="22" color="#666666" />
				<input v-model="outFilterText" confirm-type="search" class="input" type="text" placeholder="输入出库单信息">
				<uni-icons :color="'#999999'" v-if="outFilterText!==''" type="clear" size="22" @click="clear1" />
			</view>
			<view class="input-view"  v-if="current === 1">
				<uni-icons type="search" size="22" color="#666666" />
				<input v-model="purchaseFilterText" confirm-type="search" class="input" type="text" placeholder="输入请购单信息">
				<uni-icons :color="'#999999'" v-if="purchaseFilterText!==''" type="clear" size="22" @click="clear2" />
			</view>
			<view class="input-view"  v-if="current === 2">
				<uni-icons type="search" size="22" color="#666666" />
				<input v-model="sellFilterText" confirm-type="search" class="input" type="text" placeholder="输入销售订单信息">
				<uni-icons :color="'#999999'" v-if="sellFilterText!==''" type="clear" size="22" @click="clear3" />
			</view>
			<view class="input-view"  v-if="current === 3">
				<uni-icons type="search" size="22" color="#666666" />
				<input v-model="exchangeFilterText" confirm-type="search" class="input" type="text" placeholder="输入转库申请单信息">
				<uni-icons :color="'#999999'" v-if="exchangeFilterText!==''" type="clear" size="22" @click="clear4" />
			</view>
		</uni-nav-bar>
		<view class="content-control">
			<uni-segmented-control :current="current" :values="items" @clickItem="onClickItem" style-type="button" active-color="#20a0ff"></uni-segmented-control>
		</view>
		<view class="current-content">
			<view v-if="current === 0">
				<view v-for="(item,index) in outFilterList" :key="index" class="card-set">
					<uni-card
					    :title="item.mso_iden"
					    mode="basic" 
					    :is-shadow="true" 
						:extra="item.mso_date"
					>
					    <view @click="viewDetail(item.mso_iden,item.mso_orga)">
							<view>库存组织：{{ item.mso_orga }}</view>
							<view>出库仓库：{{ item.mso_warehouse }}</view>
							<view>出库分类：{{ item.mso_type }}</view>
							<view>出库部门：{{ item.mso_req_department }}</view>
							<view>备注：{{ item.mso_remarks }}</view>
							<view>创建人：{{ item.mso_creator }}</view>
							<view>创建日期：{{ item.mso_createDate }}</view>
						</view>
						<view v-if="judgeStatus(item.mso_status) === 0" class="button-box">
							<view class="delete" @click="deleteOrder(item.mso_iden)"><evan-icons type="remove" color="red" size="16"></evan-icons>删除</view>
							<view class="edit" @click="editOrder(item.mso_iden)"><evan-icons type="edit" color="blue" size="13"></evan-icons>编辑</view>
							<view class="commit" @click="commitOrder(item.mso_iden)"><evan-icons type="check" color="green" size="16"></evan-icons>提交</view>
						</view>
						<view v-if="judgeStatus(item.mso_status) === 1" class="button-box">
							<view class="detail" @click="viewDetail(item.mso_iden,item.mso_orga)"><evan-icons type="reorder" size="15"></evan-icons>详情</view>
						</view>
					</uni-card>
				</view>
				<view>
					<drag-button
						:isDock="true"
						:existTabBar="true"
						@btnClick="newOrder(current)">
					</drag-button>
				</view>
			</view>
			<view v-if="current === 1">
				
				<!-- TODO,已审批的单据->关闭按钮权限 -->
				
				<view v-for="(item,index) in purchaseFilterList" :key="index" class="card-set">
					<uni-card
					    :title="item.pr_iden"
					    mode="basic" 
					    :is-shadow="true" 
						:extra="item.pr_date"
					>
					    <view @click="viewDetail(item.pr_iden,item.orga_name)">
							<view>库存组织：{{ item.orga_name }}</view>
							<view>需求类型：{{ item.pr_type }}</view>
							<view>申请部门：{{ item.pr_department }}</view>
							<view>备注：{{ item.pr_remarks }}</view>
							<view>创建人：{{ item.pr_creator }}</view>
							<view>创建日期：{{ item.pr_createDate }}</view>
						</view>
						<view v-if="judgeStatus(item.pr_status) === 0" class="button-box">
							<view class="delete" @click="deleteOrder(item.pr_iden)"><evan-icons type="remove" color="red" size="16"></evan-icons>删除</view>
							<view class="edit" @click="editOrder(item.pr_iden)"><evan-icons type="edit" color="blue" size="13"></evan-icons>编辑</view>
							<view class="commit" @click="commitOrder(item.pr_iden)"><evan-icons type="check" color="green" size="16"></evan-icons>提交</view>
						</view>
						<view v-if="judgeStatus(item.pr_status) === 1" class="button-box">
							<view class="detail" @click="viewDetail(item.pr_iden,item.orga_name)"><evan-icons type="reorder" size="15"></evan-icons>详情</view>
							<view class="delete" @click="closeOrder(item.pr_iden)"><evan-icons type="close" color="red" size="16"></evan-icons>关闭</view>
						</view>
						<view v-if="judgeStatus(item.pr_status) === 2" class="button-box">
							<view class="detail" @click="viewDetail(item.pr_iden,item.orga_name)"><evan-icons type="reorder" size="15"></evan-icons>详情</view>
						</view>
					</uni-card>
				</view>
				<view>
					<drag-button
						:isDock="true"
						:existTabBar="true"
						@btnClick="newOrder(current)">
					</drag-button>
				</view>
			</view>
			<view v-if="current === 2">
				<view v-for="(item,index) in sellFilterList" :key="index" class="card-set">
					<uni-card
					    :title="item.so_iden"
					    mode="basic" 
					    :is-shadow="true" 
						:extra="item.so_date"
					>
					    <view @click="viewDetail(item.so_iden,item.so_orga)">
							<view>库存组织：{{ item.so_orga }}</view>
							<view>出库分类：{{ item.so_type }}</view>
							<view>客户：{{ item.so_custom }}</view>
							<view>发货仓库：{{ item.so_warehouse }}</view>
							<view>备注：{{ item.so_remarks }}</view>
							<view>创建人：{{ item.so_creator }}</view>
							<view>创建日期：{{ item.so_createDate }}</view>
						</view>
						<view v-if="judgeStatus(item.so_status) === 0" class="button-box">
							<view class="delete" @click="deleteOrder(item.so_iden)"><evan-icons type="remove" color="red" size="16"></evan-icons>删除</view>
							<view class="edit" @click="editOrder(item.so_iden)"><evan-icons type="edit" color="blue" size="13"></evan-icons>编辑</view>
							<view class="commit" @click="commitOrder(item.so_iden)"><evan-icons type="check" color="green" size="16"></evan-icons>提交</view>
						</view>
						<view v-if="judgeStatus(item.so_status) === 1" class="button-box">
							<view class="detail" @click="viewDetail(item.so_iden,item.so_orga)"><evan-icons type="reorder" size="15"></evan-icons>详情</view>
						</view>
					</uni-card>
				</view>
				<view>
					<drag-button
						:isDock="true"
						:existTabBar="true"
						@btnClick="newOrder(current)">
					</drag-button>
				</view>
			</view>
			<view v-if="current === 3">
				<view v-for="(item,index) in exchangeFilterList" :key="index" class="card-set">
					<uni-card
					    :title="item.str_iden"
					    mode="basic" 
					    :is-shadow="true" 
						:extra="item.str_date"
					>
					    <view @click="viewDetail(item.str_iden,item.str_orga)">
							<view>库存组织：{{ item.str_orga }}</view>
							<view>转入仓库：{{ item.str_to }}</view>
							<view>转出仓库：{{ item.str_from }}</view>
							<view>申请部门：{{ item.str_req_department }}</view>
							<view>创建人：{{ item.str_creator }}</view>
							<view>创建日期：{{ item.str_createDate }}</view>
						</view>
						<view v-if="judgeStatus(item.str_status) === 0" class="button-box">
							<view class="delete" @click="deleteOrder(item.str_iden)"><evan-icons type="remove" color="red" size="16"></evan-icons>删除</view>
							<view class="edit" @click="editOrder(item.str_iden)"><evan-icons type="edit" color="blue" size="13"></evan-icons>编辑</view>
							<view class="commit" @click="commitOrder(item.str_iden)"><evan-icons type="check" color="green" size="16"></evan-icons>提交</view>
						</view>
						<view v-if="judgeStatus(item.str_status) === 1" class="button-box">
							<view class="detail" @click="viewDetail(item.str_iden,item.str_orga)"><evan-icons type="reorder" size="15"></evan-icons>详情</view>
						</view>
					</uni-card>
				</view>
				<view>
					<drag-button
						:isDock="true"
						:existTabBar="true"
						@btnClick="newOrder(current)">
					</drag-button>
				</view>
			</view>
			<!-- 弹出框，关闭请购单时输入关闭原因 -->
			<view class="modelBox" v-if="showHide">
				<view class="shade" @tap="modelHide"></view>
				<view class="model">
					<view class="modelTitle">请输入关闭原因</view>
					<view class="modelInput">
						<input  placeholder-class="inputStyle" v-model="closeReason" focus/>
					</view>
					<view class="modeBtnBox">
						<view class="" @tap="modelHide">取消</view>
						<view class="" @tap="confirm">确定</view>
					</view>
				</view>
			</view>
		</view>
    </view>
</template>
 
<script>
import uniSegmentedControl from '../../components/uni-segmented-control/uni-segmented-control.vue'
import uniCard from '../../components/uni-card/uni-card.vue'
import uniIcons from '@/components/uni-icons/uni-icons.vue'
import dragButton from '../../components/drag-button/drag-button.vue'
import cmdIcon from "../../components/cmd-icon/cmd-icon.vue"
import uniNavBar from '@/components/uni-nav-bar/uni-nav-bar.vue'
import EvanIcons from '../../components/evan-icons/evan-icons.vue'
import outData from '../../data/outStore.js'
import purchaseData from '../../data/purchase.js'
import sellData from '../../data/sell.js'
import exchangeData from '../../data/exchange.js'

export default {
	components: {
		uniSegmentedControl,
		uniCard,
		dragButton,
		cmdIcon,
		uniNavBar,
		uniIcons,
		EvanIcons
	},
	data() {
		return {
			items: [],
			current: 0,
			//将data文件夹中的数据读入
			outList: outData.data,
			// purchaseList: purchaseData.data,
			sellList: sellData.data,
			exchangeList: exchangeData.data,
			// outList: [],
			purchaseList: [],
			// sellList: [],
			// exchangeList: [],
			outFilterText: '',
			purchaseFilterText: '',
			sellFilterText: '',
			exchangeFilterText: '',
			closeReason: '',
			closeIden: '',
			showHide: false,
		}
	},
	computed: {
		// 单据列表
		outFilterList () {
			let arr = []
			this.outList.forEach((item) => arr.push(item))
			if (this.outFilterText) {
				arr = this.outList.filter(item => item.mso_orga.includes(this.outFilterText)||
					item.mso_iden.includes(this.outFilterText)||
					item.mso_remarks.includes(this.outFilterText)||
					item.mso_warehouse.includes(this.outFilterText)||
					item.mso_req_department.includes(this.outFilterText)||
					item.mso_creator.includes(this.outFilterText)
				)
			}
			return arr
		},
		purchaseFilterList () {
			let arr = []
			this.purchaseList.forEach((item) => arr.push(item))
			if (this.purchaseFilterText) {
				arr = this.purchaseList.filter(item => item.orga_name.includes(this.purchaseFilterText)||
					item.pr_iden.includes(this.purchaseFilterText)||
					item.pr_remarks.includes(this.purchaseFilterText)||
					item.pr_type.includes(this.purchaseFilterText)||
					item.pr_department.includes(this.purchaseFilterText)||
					item.pr_creator.includes(this.purchaseFilterText)
				)
			}
			return arr
		},
		sellFilterList () {
			let arr = []
			this.sellList.forEach((item) => arr.push(item))
			if (this.sellFilterText) {
				arr = this.sellList.filter(item => item.so_orga.includes(this.sellFilterText)||
					item.so_remarks.includes(this.sellFilterText)||
					item.so_iden.includes(this.sellFilterText)||
					item.so_warehouse.includes(this.sellFilterText)||
					item.so_type.includes(this.selFilterText)||
					item.so_creator.includes(this.sellFilterText)||
					item.so_custom.includes(this.sellFilterText)
				)
			}
			return arr
		},
		exchangeFilterList () {
			let arr = []
			this.exchangeList.forEach((item) => arr.push(item))
			if (this.exchangeFilterText) {
				arr = this.exchangeList.filter(item => item.str_orga.includes(this.exchangeFilterText)||
					item.str_iden.includes(this.exchangeFilterText)||
					item.str_to.includes(this.exchangeFilterText)||
					item.str_from.includes(this.exchangeFilterText)||
					item.str_req_department.includes(this.exchangeFilterText)||
					item.str_creator.includes(this.exchangeFilterText)
				)
			}
			return arr
		}
	},
	methods: {
		//切换tab  current: 下方卡片内容,  currentIndex: tab栏,  范围(0-3)
		onClickItem(e) {
			let _this = this
			if (this.current !== e.currentIndex) {
				this.current = e.currentIndex;
			}
			
			if(e.currentIndex === 0){
				// let mes = this.judgeMes(0)
				// this.$http.post('/outRequest/oss', mes).then(([err,res]) => {
				// 	if (res.data.signal === '0') {
				// 		_this.outList = res.data.prs
				//     } else {
				// 		uni.showToast({
				// 			icon: 'none',
				// 			position: 'bottom',
				// 			title: res.data.message
				// 		});
				//     }
				// })
			} else if(e.currentIndex === 1){
				let mes = this.judgeMes(1)
				this.$http.post('/purchaseRequest/prs', mes).then(([err,res]) => {
					if (res.data.signal === 0) {
						_this.purchaseList = res.data.prs
				    } else {
						uni.showToast({
							icon: 'none',
							position: 'bottom',
							title: res.data.message
						});
				    }
				})
			} else if(e.currentIndex === 2){
				let mes = this.judgeMes(2)
				this.$http.post('/sell/sellOrders', mes).then(([err,res]) => {
					if (res.data.signal === '0') {
						_this.sellList = res.data.sos
				    } else {
						uni.showToast({
							icon: 'none',
							position: 'bottom',
							title: res.data.message
						});
				    }
				})
			} else if(e.currentIndex === 3){
				// let mes = this.judgeMes(3)
				// this.$http.post('/exchangeRequest/eos', mes).then(([err,res]) => {
				// 	if (res.data.signal === '0') {
				// 		_this.exchangeList = res.data.prs
				//     } else {
				// 		uni.showToast({
				// 			icon: 'none',
				// 			position: 'bottom',
				// 			title: res.data.message
				// 		});
				//     }
				// })
			}
		},
		//单据显示信息判断(根据权限)
		judgeMes(orderIndex) {
			let myinfo = uni.getStorageSync('user_info')
			let power = uni.getStorageSync('power')
			let mes = {}
			mes.area_name = myinfo.data.user.area_name			mes.user_now_iden = myinfo.data.user.username
			mes.power = power[orderIndex]
			
			return mes
		},
		//判断订单状态
		judgeStatus(status) {
			if (status === 0) {
				return 0;
			}
			else if(status === 1) {
				return 1;
			}
			else if(status === 2) {
				return 2;
			}
		},
		//查看订单详情
		viewDetail(iden,orga) {
			let diff = iden[0]+iden[1]
			let msg = {}
			msg.iden = iden
			msg.orga = orga
			if(diff === "MS") {
				try {
				    uni.setStorageSync('order_info', msg);
				} catch (e) {
				    console.log("传出库单单号失败")
				}
				uni.navigateTo({
				    url: '../detail/outDetails',
				});
			} else if(diff === "PR") {
				try {
				    uni.setStorageSync('order_info', msg);
				} catch (e) {
				    console.log("传请购单单号失败")
				}
				uni.navigateTo({
				    url: '../detail/purchaseDetails',
				});
			} else if(diff === "SO") {
				try {
				    uni.setStorageSync('order_info', msg);
				} catch (e) {
				    console.log("传销售单单号失败")
				}
				uni.navigateTo({
				    url: '../detail/sellDetails',
				});
			} else if(diff === "ST") {
				try {
				    uni.setStorageSync('order_info', msg);
				} catch (e) {
				    console.log("传转库申请单单号失败")
				}
				uni.navigateTo({
				    url: '../detail/exchangeDetails',
				});
			}
		},
		//新增单据
		newOrder(page) {
			if(page === 0) {
				uni.navigateTo({
				    url: '../out/out',
				});
			} else if(page === 1) {
				uni.navigateTo({
				    url: '../purchase/purchase',
				});
			} else if(page === 2) {
				uni.navigateTo({
				    url: '../sell/sell',
				});
			} else if(page === 3) {
				uni.navigateTo({
				    url: '../exchange/exchange',
				});
			}
		},
		//删除单据
		deleteOrder(iden) {
			let diff = iden[0]+iden[1]
			let _this = this
			if(diff === "MS") {
				uni.showModal({
				    title: '提示',
				    content: '确认删除草稿：'+iden+" ?",
				    success: function (Res) {
				    //     if (Res.confirm) {
				    //     	let mso_iden = iden
				    //     	_this.$http.post('/outRequest/soDelete', {mso_iden}).then(([err,res]) => {
								// if(res.data.signal === 0){
								// 	_this.outList = _this.outList.filter(item => !(item.mso_iden.includes(mso_iden)))
								// }
				    //     		uni.showToast({
				    //     			icon: 'none',
				    //     			position: 'bottom',
				    //     			title: res.data.message
				    //     		});
				    //     	})
				    //     } else if (Res.cancel) {
				            
				    //     }
				    }
				});
			} else if(diff === "PR") {
				uni.showModal({
				    title: '提示',
				    content: '确认删除草稿：'+iden+" ?",
				    success: function (Res) {
				        if (Res.confirm) {
							let pr_iden = iden
							_this.$http.post('/purchaseRequest/prDelete', {pr_iden}).then(([err,res]) => {
								//删除列表中该单据信息
								if(res.data.signal === 0) {
									_this.purchaseList = _this.purchaseList.filter(item => !(item.pr_iden.includes(pr_iden)))
								}
								uni.showToast({
									icon: 'none',
									position: 'bottom',
									title: res.data.message
								});
							})
				        } else if (Res.cancel) {
				            
				        }
				    }
				});
			} else if(diff === "SO") {
				uni.showModal({
				    title: '提示',
				    content: '确认删除草稿：'+iden+" ?",
				    success: function (Res) {
				        if (Res.confirm) {
							let so_iden = iden
							_this.$http.post('/sell/sellOrderDelete', {so_iden}).then(([err,res]) => {
								if(res.data.signal === 0) {
									_this.sellList = _this.sellList.filter(item => !(item.so_iden.includes(so_iden)))
								}
								uni.showToast({
									icon: 'none',
									position: 'bottom',
									title: res.data.message
								});
							})
				        } else if (Res.cancel) {
				            
				        }
				    }
				});
			} else if(diff === "ST") {
				uni.showModal({
				    title: '提示',
				    content: '确认删除草稿：'+iden+" ?",
				    success: function (Res) {
				        if (Res.confirm) {
				    //     	let str_iden = iden
				    //     	_this.$http.post('/exchangeRequest/strDelete', {str_iden}).then(([err,res]) => {
				    //     		if(res.data.signal === 0) {
								// 	_this.exchangeList = _this.exchangeList.filter(item => !(item.str_iden.includes(str_iden)))
								// }
				    //     		uni.showToast({
				    //     			icon: 'none',
				    //     			position: 'bottom',
				    //     			title: res.data.message
				    //     		});
				    //     	})
				        } else if (Res.cancel) {
				            
				        }
				    }
				});
			}
		},
		//提交草稿
		commitOrder(iden) {
			let diff = iden[0]+iden[1]
			let _this = this
			if(diff === "MS") {
				uni.showModal({
				    title: '提示',
				    content: '确认提交草稿：'+iden+" ?",
				    success: function (Res) {
				        if (Res.confirm) {
				        	// let mso_iden = iden
				        	// _this.$http.post('/outRequest/sodSubmit', {mso_iden}).then(([err,res]) => {
				        	// 	//修改列表中该单据信息
				        	// 	if(res.data.signal === 0) {
				        	// 		for(let i=0; i<_this.outList.length; i++) {
				        	// 			if(_this.outList[i].mso_iden === iden){
				        	// 				_this.outList[i].mso_status = '1'
				        	// 				break
				        	// 			}
				        	// 		}
				        	// 	}
				        	// 	uni.showToast({
				        	// 		icon: 'none',
				        	// 		position: 'bottom',
				        	// 		title: res.data.message
				        	// 	});
				        	// })
				        } else if (Res.cancel) {
				            
				        }
				    }
				});
			} else if(diff === "PR") {
				uni.showModal({
				    title: '提示',
				    content: '确认提交草稿：'+iden+" ?",
				    success: function (Res) {
				       if (Res.confirm) {
							let pr_iden = iden
							_this.$http.post('/purchaseRequest/prdSubmit', {pr_iden}).then(([err,res]) => {
								//修改列表中该单据信息
								if(res.data.signal === 0) {
									for(let i=0; i<_this.purchaseList.length; i++) {
										if(_this.purchaseList[i].pr_iden === iden){
											_this.purchaseList[i].pr_status = '1'
											break
										}
									}
								}
								uni.showToast({
									icon: 'none',
									position: 'bottom',
									title: res.data.message
								});
							})
				       } else if (Res.cancel) {
				           
				       }
				    }
				});
			} else if(diff === "SO") {
				uni.showModal({
				    title: '提示',
				    content: '确认提交草稿：'+iden+" ?",
				    success: function (Res) {
				        if (Res.confirm) {
				        	let so_iden = iden
				        	_this.$http.post('/sell/soDetailSubmit', {so_iden}).then(([err,res]) => {
				        		//修改列表中该单据信息
				        		if(res.data.signal === 0) {
				        			for(let i=0; i<_this.sellList.length; i++) {
				        				if(_this.sellList[i].so_iden === iden){
				        					_this.sellList[i].so_status = '1'
				        					break
				        				}
				        			}
				        		}
				        		uni.showToast({
				        			icon: 'none',
				        			position: 'bottom',
				        			title: res.data.message
				        		});
				        	})
				        } else if (Res.cancel) {
				            
				        }
				    }
				});
			} else if(diff === "ST") {
				uni.showModal({
				    title: '提示',
				    content: '确认提交草稿：'+iden+" ?",
				    success: function (Res) {
				        if (Res.confirm) {
				        	// let str_iden = iden
				        	// _this.$http.post('/exchangeRequest/strdSubmit', {str_iden}).then(([err,res]) => {
				        	// 	//修改列表中该单据信息
				        	// 	if(res.data.signal === 0) {
				        	// 		for(let i=0; i<_this.exchangeList.length; i++) {
				        	// 			if(_this.exchangeList[i].str_iden === iden){
				        	// 				_this.exchangeList[i].str_status = '1'
				        	// 				break
				        	// 			}
				        	// 		}
				        	// 	}
				        	// 	uni.showToast({
				        	// 		icon: 'none',
				        	// 		position: 'bottom',
				        	// 		title: res.data.message
				        	// 	});
				        	// })
				        } else if (Res.cancel) {
				            
				        }
				    }
				});
			}
		},
		//编辑草稿
		editOrder(iden) {
			let diff = iden[0]+iden[1]
			if(diff === "MS") {
				uni.navigateTo({
				    url: '../user/myinfo',
				});
			} else if(diff === "PR") {
				uni.navigateTo({
				    url: '../user/myinfo',
				});
			} else if(diff === "SO") {
				uni.navigateTo({
				    url: '../user/myinfo',
				});
			} else if(diff === "ST") {
				uni.navigateTo({
				    url: '../user/myinfo',
				});
			}
		},
		//关闭订单
		closeOrder(iden) {
			this.showHide = true
			this.closeIden = iden
		},
		clear1() {
			this.outFilterText = ''
		},
		clear2() {
			this.purchaseFilterText = ''
		},
		clear3() {
			this.sellFilterText = ''
		},
		clear4() {
			this.exchangeFilterText = ''
		},
		//隐藏输入框
		modelHide(){
			this.showHide=false
		},
		// 输入框确定按钮
		confirm(){
			let _this = this
			let myinfo = uni.getStorageSync('user_info')
			uni.showModal({
			    title: '提示',
			    content: '确认关闭请购单：'+_this.closeIden+" ?",
			    success: function (Res) {
			        if (Res.confirm) {
						let msg = {}
						msg.pr_iden = _this.closeIden
						msg.user_now_iden = myinfo.data.user.username
						msg.pr_closerReason = _this.closeReason
						_this.$http.post('/purchaseRequest/prClose', msg).then(([err,res]) => {
							//修改列表中该单据信息
							if(res.data.signal === 0) {
								for(let i =0; i<_this.purchaseList.length; i++) {
									if(_this.purchaseList[i].pr_iden === _this.closeIden){
										_this.purchaseList[i].pr_status = '2'
										break
									}
								}
							}
							uni.showToast({
								icon: 'none',
								position: 'bottom',
								title: res.data.message
							});
						})
						//清空缓存
						_this.closeIden = ''
						_this.closeReason = ''
			        } else if (Res.cancel) {
			            _this.closeIden = ''
			            _this.closeReason = ''
			        }
			    }
			});
			this.showHide=false
		},
		//判断权限
		judgePower() {
			let myinfo = uni.getStorageSync('user_info')
			let power = [0,0,0,0]
			for(let i=0; i<myinfo.data.roles.length; i++){
				let po = myinfo.data.roles[i][1]
				power[0] = power[0]<po[6]? po[6]:power[0]
				power[1] = power[1]<po[1]? po[1]:power[0]
				power[2] = power[2]<po[0]? po[0]:power[0]
				power[3] = power[3]<po[9]? po[9]:power[0]
			}
			
			if(power[0] === 2) {
				for(let i=0; i<myinfo.data.roles.length; i++){
					let po = myinfo.data.roles[i][1]
					if(po[6] === 1){
						power[0] = 3
					}
				}
			}
			if(power[1] === 2) {
				for(let i=0; i<myinfo.data.roles.length; i++){
					let po = myinfo.data.roles[i][1]
					if(po[1] === 1){
						power[1] = 3
					}
				}
			}
			if(power[2] === 2) {
				for(let i=0; i<myinfo.data.roles.length; i++){
					let po = myinfo.data.roles[i][1]
					if(po[0] === 1){
						power[2] = 3
					}
				}
			}
			if(power[3] === 2) {
				for(let i=0; i<myinfo.data.roles.length; i++){
					let po = myinfo.data.roles[i][1]
					if(po[9] === 1){
						power[3] = 3
					}
				}
			}
			uni.setStorageSync('power',power)
		}
	},
	
	onLoad: function() {   
		//登录检查，需要重写一下
		// loginMsg = this.checkLogin('../pages/main/main', 'switchTab');
		// if(!loginMsg){
		// 	return;
		// }
		
		//填入权限
		this.judgePower()
		let _this = this
		let myinfo = uni.getStorageSync('user_info')
		let power = uni.getStorageSync('power')
		//判断界面权限
		if(power[0] !== 0){
			this.items[0] = '出库'
		}
		if(power[1] !== 0){
			this.items[1] = '请购'
		}
		if(power[2] !== 0){
			this.items[2] = '销售'
		}
		if(power[3] !== 0){
			this.items[3] = '转库'
		}
		this.$forceUpdate()
		
		
		//TODO 主页加载时默认搜索出库单
		// let outMes = {}
		// outMes.area_name = myinfo.data.user.area_name
		// outMes.user_now_iden = myinfo.data.user.username
		// outMes.power = power[0]
		// this.$http.post('/purchaseRequest/prs', outMes).then(([err,res]) => {
		// 	if (res.data.signal === '0') {
		// 		_this.testList = res.data.prs
		//     } else {
		// 		console.log(res.data.message)
		//     }
		// })
		
		
		uni.removeStorageSync('viewout');
		uni.removeStorageSync('viewpurchase');
		uni.removeStorageSync('viewsell');
		uni.removeStorageSync('viewexchange');
	}
}

</script>

<style>
	page {
		display: flex;
		flex-direction: column;
		box-sizing: border-box;
		background-color: #efeff4;
		min-height: 100%;
		height: auto;
	}
	
	view {
		font-size: 28rpx;
		line-height: inherit;
	}
	.content {
		padding: 0;
	}
	.content-control {
		padding: 5upx;
		padding-bottom: 0;
		width: auto;
	}
	.current-content {
		justify-content: center;
		align-items: center;
		text-align: left;
	}
	.button-box {
		display: flex;
		justify-content: space-between;
		padding-top: 1vw;
	}
	.delete {
		width: 90upx;
		color: red;
	}
	.edit {
		padding-top: 3rpx;
		color: blue;
		width: 90upx;
	}
	.detail {
		width: 90upx;
	}
	.commit {
		width: 90upx;
		color: green;
	}
	
	.input-view {
		align-items: center;
		justify-content: center;
		width: 100%;
		display: flex;
		background-color: #e7e7e7;
		height: 30px;
		border-radius: 15px;
		padding: 0 4%;
		flex-wrap: nowrap;
		margin: 7px 10rpx;
		line-height: 30px;
		background: #f5f5f5;
	}
	.input-view .input {
		height: 30px;
		line-height: 30px;
		width: 94%;
		padding: 0 3%;
	}
	.modelBox {
		display: inline-flex;
		flex-direction: row;
		justify-content: space-between;
		height: 50upx;
		width: 220upx;
		position: relative
	}
	.shade{
		width: 100%;
		height: 100%;
		position: fixed;
		top: 0;
		left: 0;
		z-index: 100;
		background-color: rgba(0,0,0,.6);
	}
	.model{
		width: 80%;
		border-radius: 35upx;
		background-color: #fff;
		padding: 30upx;
		box-sizing: border-box;
		position: fixed;
		top: 50%;
		left: 50%;
		transform: translate(-50%,-50%);
		z-index: 200;
	}
	.modelTitle{
		font-size: 34upx;
		color: #333;
		margin-bottom: 20upx;
	}
	.modelInput{
		width: 100%;
		height: 40upx;
		font-size: 30upx;
		color: #333;
		margin-bottom: 40upx;
	}
	.modelInput input{
		width: 100%;
		height: 100%;
		border: none;
		border-bottom:2upx solid #8fba5d ;
	}
	.modeBtnBox{
		width: 100%;
		height: 40upx;
		display: flex;
		align-items: center;
		justify-content: flex-end;
		color:#8fba5d ;
		font-size: 30upx;
	}
	.modeBtnBox view{
		width: 25%;
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
	}

</style>
