// 添加左侧菜单叶子节点点击事件
$(".leaf").each(function(i){
    $(this).on("click", function(){
        console.info($(this).parent().parent().attr("class"));
        leaf_active($(this).attr("id"));
    });
});

// 执行叶子节点点击事件
function leaf_active(id){
    var leaf = $("#" + id + ".leaf");
    var grandfather = leaf.parent().parent();
    // 如果叶子节点激活，则该节点的祖父节点也应被激活
    if (grandfather.hasClass("treeview")) {
        grandfather.addClass("active");
    }

    leaf.addClass("active");
}
