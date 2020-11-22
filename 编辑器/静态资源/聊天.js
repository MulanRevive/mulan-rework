$(document).ready(function () {
  if (!window.console) window.console = {};
  if (!window.console.log) window.console.log = function () { };

  $("#输入").on("keypress", function (e) {
    if (e.keyCode == 13) {
      发送请求($(this));
      return false;
    }
  });
  $( "#输入" ).autocomplete({
    source: function( request, response ) {
      $.ajax( {
        url: "http://localhost:8888/requests",
        //dataType: "json",

        // https://api.jqueryui.com/autocomplete/#option-source 发送输入内容
        data: {
          term: request.term
        },
        success: function( data ) {
          response( data["历史"] );
        }
      } );
    },
    // 影响输入(如果新内容触发了补全, 即使直接回车就仍会用第一个补全项)
    //autoFocus: true
  });
  $("#输入").select();
  更新.开始();
  编辑器.setValue("");
});

function 发送请求(输入框) {
  输入 = 输入框.val()
  发送内容 = { "类型": "保存", "请求内容": 输入 }
  if (输入.startsWith("保存")) {
    发送内容["编辑器内容"] = 编辑器.getValue()
  }
  更新.口.send(JSON.stringify(发送内容));
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
    // console.log(话语)
    if (话语.类型 == "编辑器") {
      编辑器.setValue(话语.内容);
    } else {
      var 节点 = $(话语.html);
      节点.addClass(话语.类型 == "要求" ? "要求" : "回应");
      节点.hide();
      $("#历史").append(节点);
      节点.slideDown();
    }
  }
};
