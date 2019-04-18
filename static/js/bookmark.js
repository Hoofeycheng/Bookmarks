(function () {
    let jquery_version = "3.3.1";
    let site_url = "https://7a876442.ngrok.io/";
    alert(site_url);
    // let site_url = "http://127.0.0.1:8000/";
    let static_url = site_url + "static/";
    let min_width = 100;
    let min_height = 100;

    function bookmarklet(msg) {
        // 分享图片的代码
        // 加载css
        let css = jQuery("link");
        css.attr({
            rel: 'stylesheet',
            type: 'text/css',
            href: static_url + "css/bookmarklet.css?r=" + Math.floor(Math.random()*999999)
        });
        jQuery('head').append(css);
        alert(css);
        // 加载html结构
        box_html = "<div id='bookmarklet'><a href='#' id='close'>X</a><h1>搜索到的图片：</h1><div class='images'></div></div>";
        jQuery('body').append(box_html);

        // 关闭事件
        jQuery("#bookmarklet #close").click(function () {
            jQuery("#bookmarklet").remove();
        });

        // 寻找页面内的所有图片然后显示在新增的html结构中
        jQuery.each(jQuery('img[src$="jpg"]'), function (index, image) {
            if(jQuery(image).width() >= min_width && jQuery(image).height() >= min_height){
                image_url = jQuery(image).attr("src");
                jQuery("#bookmarklet .images").append("<a href='#'><img src='" + image_url + "'></a>")
            }
        });
        //点击图片时按照指定的url访问我们的网站
        jQuery('#bookmarklet .images a').click(function (e) {
            let selected_image = jQuery(this).children('img').attr('src');
            //隐藏自定义的bookmarklet的HTML
            jQuery('#bookmarklet').hide();
            //打开新的页面来提交选中的image
            window.open(site_url + 'images/create/?url=' + encodeURIComponent(selected_image),'_blank');
        });
    }

    // 检查页面是否加载了jquery, 如果没有加载就进行加载
    if(typeof window.jQuery !== "undefined"){
        bookmarklet();
    }
    else{
        let script = document.createElement("script");
        script.src = "//cdn.bootcss.com/jquery/" + jquery_version + "/jquery.min.js";
        document.head.appendChild(script);
        let attempts = 15;
        (function () {
            if(typeof window.jQuery === "undefined"){
                if(--attempts>0){
                    window.setTimeout(arguments.callee, 250)
                }else {
                    alert("加载jquery失败")
                }
            }else{
                bookmarklet()
            }
        })();
    }
})();