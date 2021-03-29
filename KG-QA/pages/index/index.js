//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    query: '',
    response: '',
  },
  //事件处理函数
  onLoad: function () {
    
  },
  getInput: function (e) {
    var that = this
    var q = e.detail.value
    that.setData({
      query: q
    })
  },
  sendRequest: function (e) {
    var that = this
    var query = that.data.query
    var queryUrl = 'https://sumsky.top:5000/api?q=' + query
    wx.request({
      url: queryUrl,
      data:{},
      timeout: 60000,
      success: function (r) {
        console.log('请求成功', r)
        that.setData({
          response: r.data
        })
      },
      fail: function (r) {
        console.log('请求失败。请稍后再试')
      }
    })
  }
})
