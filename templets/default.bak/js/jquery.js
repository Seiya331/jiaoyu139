(function ($) {
    var defaultparms = {
        watermark: 1,
        mark: '',
        btnbg: "#FFFFFF",
        btnhoverbg: "#000",
        hasNum: true,
        markon: 'right',
        numnav: true,
        isbg: true,
        hastitle: false,
        hassubtitle: false,
        height: 350,
        width: 600,
        pause: 2000,
        speed: 600
    }
    var index = 0;
    $.fn.TLSlider = function (op) {
        var indexTemp = index;
        var ops = $.extend({}, defaultparms, op);

        var cur = new Array();
        cur[indexTemp] = 1;

        var ob = $(this);
        var img = ob.find('img');
        var h = $(this).height();
        var w = $(this).width();
        var n = img.length;
        var ele = $('ul', ob);
        var lh = ops.height == 0 ? h : ops.height;
        var lw = ops.width == 0 ? w : ops.width;

        ele.css({ 'width': w * n });
        ob.css({ 'overflow': 'hidden', 'position': 'relative' });
        $('li', ob).css({ 'float': 'left', 'height': lh, 'width': lw, 'overflow': 'hidden', 'margin': '0px', 'padding': '0px', 'list-style': 'none' });
        $('ul', ob).css({ 'margin': '0px', 'padding': '0px', 'list-style': 'none' });
        img.css({ 'float': 'left', 'height': lh, 'width': lw });

        if (ops.numnav) {
            addnavdiv();

        }
        if (ops.watermark == 1) {
            var mark = "<span class='slider-watermark'>" + ops.mark + "</span>";
            ob.append(mark);
            addwatermarkcss();
        }
        if (ops.watermark == 2) {
            var mark = "<span class='slider-watermark'><img src='" + ops.mark + "'/></span>";
            ob.append(mark);
            addwatermarkcss();
        }
        var title = "";
        var link = "";
        if (ops.hassubtitle) {
            title = img.eq(0).attr('title');
            link = img.eq(0).attr('link');
            sub_title = img.eq(0).attr('sub_title');
            if (!title)
                title = "";
            if (!link)
                link = "";
            if (!sub_title)
                sub_title = "";
            var sub_title_div = "<div class='hdp_cite'>";
            sub_title_div += "<div class='tit'>" + title + "</div>";
            sub_title_div += "<div class='txt'>" + sub_title + "</div>";
            sub_title_div += "</div>";
            ob.append(sub_title_div);
        }
        else if (ops.isbg) {
           
            if (ops.hastitle) {
                title = img.eq(0).attr('title');
                link = img.eq(0).attr('link');
                if (!title)
                    title = "";
                if (!link)
                    link = "";
            }
            var bgdiv = "<div class='slider-title-bg'><span class='slider-img-title' style='width:" + (op.width - 10) + "px'><a href=\"" + link + "\" target=\"_blank\">" + title + "</a></span></div>";
            ob.append(bgdiv);
            addtitlecss();
        }
        function andtitle(i) {
            var link = img.eq(i).attr('link');
            var imgtitle = img.eq(i).attr('title');
            ob.find(".slider-img-title").html("<a href=\"" + link + "\" target=\"_blank\">" + imgtitle + "</a>");
        }
        function andsubtitle(i) {
            var title = img.eq(i).attr('title');
            var sub_title = img.eq(i).attr('sub_title');
            ob.find(".hdp_cite .tit").html(title);
            ob.find(".hdp_cite .txt").html(sub_title);
        }
        function andnavon(i) {
            ob.find(".slider-num-nav-span").eq(i).css({ 'background-color': '' + ops.btnhoverbg + '', 'color': '#B5110F' }).siblings().css({ 'background-color': '' + ops.btnbg + '', 'color': '#FFFFFF' });

        }
        function slide(i, on) {
            ele.stop();
            var next = i == n ? 1 : i + 1;
            var l = (i - 1) * w * (-1);
            cur[indexTemp] = i;
            if (ops.hassubtitle) {
                andsubtitle((i - 1));
            }
            else if (ops.isbg) {
                andtitle((i - 1));
            }
            if (ops.numnav) {
                andnavon((i - 1));
            }
            ele.animate({ marginLeft: l }, ops.speed);
            if (on) {
                clearTimeout(timeout);
            }
            if (!on) {
                timeout = setTimeout(function () {
                    slide(next, false);
                }, ops.pause);
            }
        }

        function addnavdiv() {
            var nav = "<div class='slider-num-nav'>";
            for (var i = 0; i < n; i++) {
                nav += "<span class='slider-num-nav-span' name='" + (i + 1) + "'>" + (ops.hasNum ? (i + 1) : "") + "</span>";
            }
            nav += "</div>";
            ob.append(nav);
            addnavcss();
            ob.find('.slider-num-nav-span').hover(function () {
                var num = parseInt($(this).attr("name"));
                slide(num, true);
            }, function () {
                if (cur[indexTemp] >= n) { cur[indexTemp] = 1; }
                timeout = setTimeout(function () {
                    slide((cur[indexTemp] / 1 + 1), false);
                }, ops.pause / 4);
            });


        }
        function addnavcss() {
            $(".slider-num-nav").css({
                'max-width': '150px',
                'height': '25px',
                'position': 'absolute',
                'bottom': '0px',
                'right': '20px',
                'z-index': '1200'
            });
            $(".slider-num-nav-span").css({
                'width': '15px',
                'height': '15px',
                'float': 'left',
                'background-color': '#FFFFFF',
                'margin': '0 2px',
                'cursor': 'pointer',
                'margin-top': '3px',
                'font-size': '2px',
                'color': '#FFFFFF',
                'overflow': 'hidden'
            });

        }
        function addtitlecss() {
            $(".slider-title-bg").css({
                'width': '100%',
                'height': '40px',
                'background': 'url(slider-title-bg.png) repeat-x',
                'position': 'absolute',
                'bottom': '0px', 'left': '0px'
            });
            $(".slider-img-title").css({
                'padding-left': '10px',
                'height': '30px',
                'float': 'left',
                'margin-top': '10px',
                'font-size': '18px',
                'color': '#fff'
            });
        }
        function addwatermarkcss(on) {
            $(".slider-watermark").css({
                'position': 'absolute',
                'font-size': '18px',
                'font-weight': 'bold',
                'z-index': '999',
                'top': '10px',
                'color': '#E4F8EC',
                'font-family': ''
            });
            ob.find(".slider-watermark").css(ops.markon, '15px');
        }
        andnavon(0);
        var timeout;
        timeout = setTimeout(function () {
            slide(2, false);
        }, (ops.pause));
        index++;
    }

})(jQuery);
