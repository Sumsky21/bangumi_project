// pages/chat/chat.js
// pages/contact/contact.js
const app = getApp();
var inputVal = '';
var msgList = [];
var windowWidth = wx.getSystemInfoSync().windowWidth;
var windowHeight = wx.getSystemInfoSync().windowHeight;
var keyHeight = 0;

/**
 * 初始化数据
 */
function initData(that) {
  inputVal = '';
  msgList = [{
      speaker: 'server',
      contentType: 'text',
      content: '我还有点笨，得花些时间理解你说的话，请耐心等待哦'
    },
    {
      speaker: 'server',
      contentType: 'text',
      content: '你都喜欢看什么冻鳗啊'
    },
  ]
  that.setData({
    msgList,
    inputVal
  })
}

/**
 * 计算msg总高度
 */
// function calScrollHeight(that, keyHeight) {
//   var query = wx.createSelectorQuery();
//   query.select('.scrollMsg').boundingClientRect(function(rect) {
//   }).exec();
// }

Page({
  /**
   * 页面的初始数据
   */
  data: {
    scrollHeight: '100vh',
    inputBottom: 0,
    userAvatar: '',
    animation: {},
    Placeholder: "输入框在这里！",
    infoShow: false,
    buttons: [{text: "知道了"}]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    initData(this);
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function() {
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function() {
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {
  },

  /**
   * 获取聚焦
   */
  focus: function(e) {
    keyHeight = e.detail.height;
    this.setData({
      scrollHeight: (windowHeight - keyHeight) + 'px',
      Placeholder: "我喜欢jojo，它的画风很棒！"
    });
    this.setData({
      toView: 'msg-' + (msgList.length - 1),
      inputBottom: keyHeight + 'px'
    })
    //计算msg高度
    // calScrollHeight(this, keyHeight);

  },

  //失去聚焦(软键盘消失)
  blur: function(e) {
    this.setData({
      scrollHeight: '100vh',
      inputBottom: 0,
      Placeholder: "输入框在这里！"
    })
    this.setData({
      toView: 'msg-' + (msgList.length - 1)
    })

  },

  /**
   * 显示bot简介 
   */
  openInfo: function(e) {
    var that = this
    that.setData({
      infoShow: true
    })
  },
  closeInfo: function(e) {
    var that = this
    that.setData({
      infoShow: false
    })
  },

  /**
   * 发送点击监听
   */
  sendClick: function(e) {
    var that = this
    var animes = []
    var qtype = {}
    var question = e.detail.value
    if (question == "") {
      question = "我喜欢jojo，它的画风很棒！"
    }
    var query = {
      "task": 0,
      "q": question
    }
    var queryUrl = 'https://sumsky.xyz:5000/api'
    msgList.push({
      speaker: 'customer',
      contentType: 'text',
      content: query.q
    })
    inputVal = '';
    this.setData({
      msgList,
      inputVal
    });
    //得到响应之前首先推送一条正在加载的消息, 获取该消息index以便后续处理
    var re_index = msgList.push({
      speaker: 'server',
      contentType: 'loading',
      content: '',
    }) - 1
    this.setData({
      msgList,
    });
    //向Flask API发送请求
    wx.request({
      url: queryUrl,
      data: JSON.stringify(query),
      method: 'POST',
      timeout: 60000,
      success: (r) => {
        console.log('请求成功', r)
        var rtype = r.data.rtype
        if (rtype == 0) {
          //获取到答案
          msgList[re_index].content = r.data.answer
          msgList[re_index].contentType = 'text'
          this.setData({
            msgList
          })
          //设置下拉高度
          this.setData({
            scrollHeight: '100vh',
            inputBottom: 0,
          })
          this.setData({
            toView: 'msg-' + (msgList.length - 1)
          })
        }
        else if (rtype == 1) {
          //需要再次进行选择
          msgList[re_index].contentType = 'loading'
          animes = r.data.anime_set
          qtype = r.data.qtype
          that.chooseAnime(animes, qtype, re_index)
        }
        else {
          msgList[re_index].content = '呜呜呜，我太菜了，理解不能，麻烦换个问题吧'
          msgList[re_index].contentType = 'text'
          this.setData({
            msgList
          })
        }
      },
      fail: function (r) {
        console.log('请求失败。请稍后再试')
      }
    })
  },

  /**
   * 弹出Actionsheet让用户确认模糊匹配结果；再次向API发送请求。idx是对应消息的编号
   */
  chooseAnime: function (animes, qtype, idx) {
    var that = this
    //使用promise机制实现弹框和再次发请求同步（按顺序）操作
    var promiseArr = []
    for (let i=0; i<animes.length; i++) {
      var ask = "请问您说的是《" + animes[i] + "》吗？"
      var promise = new Promise((resolve, reject) => {
        wx.showActionSheet({
          alertText: ask,
          itemList: ['猜对了', '不是这个'],
          success: function (r) {
            var index = r.tapIndex
            console.log(index)
            if (index == 1) {
              animes.splice(i, 1) //用户选择否则删除该元素
            }
            resolve(animes)
          },
          fail: function (r) {
            //用户若选择取消则弹出提示信息
            console.log('Actionsheet未选择', r)
            msgList[idx].content = '模糊匹配结果未确认，麻烦重新问一遍哦~'
            msgList[idx].contentType = 'text'
            that.setData({
              msgList
            })
            reject(r.errMsg)
          }
        })
      }) 
      promiseArr.push(promise)     
    }
    console.log(promiseArr)
    Promise.all(promiseArr).then(res => {
      console.log(animes)
      var queryUrl = 'https://sumsky.xyz:5000/api'
      var query = {
        "task": 1,
        "qtype": qtype,
        "anime_list": animes
      }
      wx.request({
        url: queryUrl,
        data: JSON.stringify(query),
        method: 'POST',
        timeout: 60000,
        success: (r) => {
          console.log('请求成功', r)
          var rtype = r.data.rtype
          if (rtype == 0) {
            //获取到答案
            msgList[idx].content = r.data.answer
            msgList[idx].contentType = 'text'
            this.setData({
              msgList
            })
            //设置下拉高度
            this.setData({
              scrollHeight: '100vh',
              inputBottom: 0,
            })
            this.setData({
              toView: 'msg-' + (msgList.length - 1)
            })
          }
          else {
            console.log('回答异常') //正常情况下此处rtype应当都是0
          }
        },
        fail: (r) => {
          console.log('请求失败', r)
        }
      })
    }).catch(res => {
      console.log(res)
    })
  },

  /**
   * 尝试为消息框加入动画
   */
  msgAnime: function (e) {
    var that = this
    console.log('触发动画')
    var a = wx.createAnimation({
      duration: 1000,
      timingFunction: 'linear',
      delay: 500
    })
    a.translateY(0).opacity(1).step().translateY(30).step()
    this.setData({
      animation: a.export()
    })
  },

  /**
   * 退回上一页
   */
  toBackClick: function() {
    wx.navigateBack({})
  }

})