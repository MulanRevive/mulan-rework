$(document).ready(function () {
  if (!window.console) window.console = {};
  if (!window.console.log) window.console.log = function () { };

  $("#输入").on("keypress", function (e) {
    if (e.keyCode == 13) {
      发送请求($(this));
      return false;
    }
  });
  $("#输入").select();
  更新.开始();
});

function 发送请求(输入框) {
  更新.口.send(JSON.stringify({ "请求内容": 输入框.val() }));
  输入框.val("").select()
}

var 更新 = {
  口: null,

  开始: function () {
    var url = "ws://" + location.host + "/chatsocket";
    更新.口 = new WebSocket(url);
    更新.口.onmessage = function (事件) {
      更新.显示新消息(JSON.parse(事件.data));
    }
  },

  显示新消息: function (话语) {
    var 节点 = $(话语.html);
    节点.addClass(话语.风格);
    节点.hide();
    $("#历史").append(节点);
    节点.slideDown();
  }
};
