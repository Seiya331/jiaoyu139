(function(){var q=this,u=function(a){var b=typeof a;if("object"==b)if(a){if(a instanceof Array)return"array";if(a instanceof Object)return b;var c=Object.prototype.toString.call(a);if("[object Window]"==c)return"object";if("[object Array]"==c||"number"==typeof a.length&&"undefined"!=typeof a.splice&&"undefined"!=typeof a.propertyIsEnumerable&&!a.propertyIsEnumerable("splice"))return"array";if("[object Function]"==c||"undefined"!=typeof a.call&&"undefined"!=typeof a.propertyIsEnumerable&&!a.propertyIsEnumerable("call"))return"function"}else return"null";
else if("function"==b&&"undefined"==typeof a.call)return"object";return b},aa=function(a){var b=typeof a;return"object"==b&&null!=a||"function"==b},ba=function(a,b,c){return a.call.apply(a.bind,arguments)},ca=function(a,b,c){if(!a)throw Error();if(2<arguments.length){var d=Array.prototype.slice.call(arguments,2);return function(){var c=Array.prototype.slice.call(arguments);Array.prototype.unshift.apply(c,d);return a.apply(b,c)}}return function(){return a.apply(b,arguments)}},w=function(a,b,c){w=Function.prototype.bind&&
-1!=Function.prototype.bind.toString().indexOf("native code")?ba:ca;return w.apply(null,arguments)};var da=(new Date).getTime();var y=function(a){a=parseFloat(a);return isNaN(a)||1<a||0>a?0:a},ea=function(a,b){return/^true$/.test(a)?!0:/^false$/.test(a)?!1:b},fa=/^([\w-]+\.)*([\w-]{2,})(\:[0-9]+)?$/,ga=function(a,b){if(!a)return b;var c=a.match(fa);return c?c[0]:b};var ha=y("0.15"),ia=y("0.01"),ja=y("0.001"),ka=y("0.001"),la=y("0.2"),ma=ea("true",!0);var na=ea("false",!1),oa=ea("false",!1);var pa=function(){},ra=function(a,b,c){switch(typeof b){case "string":qa(b,c);break;case "number":c.push(isFinite(b)&&!isNaN(b)?b:"null");break;case "boolean":c.push(b);break;case "undefined":c.push("null");break;case "object":if(null==b){c.push("null");break}if(b instanceof Array){var d=b.length;c.push("[");for(var f="",e=0;e<d;e++)c.push(f),ra(a,b[e],c),f=",";c.push("]");break}c.push("{");d="";for(f in b)b.hasOwnProperty(f)&&(e=b[f],"function"!=typeof e&&(c.push(d),qa(f,c),c.push(":"),ra(a,e,c),
d=","));c.push("}");break;case "function":break;default:throw Error("Unknown type: "+typeof b);}},sa={'"':'\\"',"\\":"\\\\","/":"\\/","\b":"\\b","\f":"\\f","\n":"\\n","\r":"\\r","\t":"\\t","\x0B":"\\u000b"},ta=/\uffff/.test("\uffff")?/[\\\"\x00-\x1f\x7f-\uffff]/g:/[\\\"\x00-\x1f\x7f-\xff]/g,qa=function(a,b){b.push('"');b.push(a.replace(ta,function(a){if(a in sa)return sa[a];var b=a.charCodeAt(0),f="\\u";16>b?f+="000":256>b?f+="00":4096>b&&(f+="0");return sa[a]=f+b.toString(16)}));b.push('"')};var ua=String.prototype.trim?function(a){return a.trim()}:function(a){return a.replace(/^[\s\xa0]+|[\s\xa0]+$/g,"")},Ca=function(a){if(!va.test(a))return a;-1!=a.indexOf("&")&&(a=a.replace(wa,"&amp;"));-1!=a.indexOf("<")&&(a=a.replace(xa,"&lt;"));-1!=a.indexOf(">")&&(a=a.replace(ya,"&gt;"));-1!=a.indexOf('"')&&(a=a.replace(za,"&quot;"));-1!=a.indexOf("'")&&(a=a.replace(Aa,"&#39;"));-1!=a.indexOf("\x00")&&(a=a.replace(Ba,"&#0;"));return a},wa=/&/g,xa=/</g,ya=/>/g,za=/"/g,Aa=/'/g,Ba=/\x00/g,va=/[\x00&<>"']/,
Da={"\x00":"\\0","\b":"\\b","\f":"\\f","\n":"\\n","\r":"\\r","\t":"\\t","\x0B":"\\x0B",'"':'\\"',"\\":"\\\\"},A={"'":"\\'"},Ea=function(a,b){return a<b?-1:a>b?1:0},Fa=function(){return"transition".replace(/\-([a-z])/g,function(a,b){return b.toUpperCase()})},Ga=function(a){var b="\\s";return a.replace(new RegExp("(^"+(b?"|["+b+"]+":"")+")([a-z])","g"),function(a,b,f){return b+f.toUpperCase()})};var B=function(a){B[" "](a);return a};B[" "]=function(){};var Ha=function(a){try{var b;if(b=!!a&&null!=a.location.href)a:{try{B(a.foo);b=!0;break a}catch(c){}b=!1}return b}catch(d){return!1}},D=function(a,b){if(!(1E-4>Math.random())){var c=Math.random();if(c<b){try{var d=new Uint16Array(1);window.crypto.getRandomValues(d);c=d[0]/65536}catch(f){c=Math.random()}return a[Math.floor(c*a.length)]}}return null},Ia=/^(-?[0-9.]{1,30})$/,E=function(a){return Ia.test(a)&&(a=Number(a),!isNaN(a))?a:null};var Ja=function(a){var b=a.toString();a.name&&-1==b.indexOf(a.name)&&(b+=": "+a.name);a.message&&-1==b.indexOf(a.message)&&(b+=": "+a.message);if(a.stack){a=a.stack;var c=b;try{-1==a.indexOf(c)&&(a=c+"\n"+a);for(var d;a!=d;)d=a,a=a.replace(/((https?:\/..*\/)[^\/:]*:\d+(?:.|\n)*)\2/,"$1");b=a.replace(/\n */g,"\n")}catch(f){b=c}}return b};var Ka=document,F=window;var G=function(a,b){for(var c in a)Object.prototype.hasOwnProperty.call(a,c)&&b.call(null,a[c],c,a)},La=function(a){return!!a&&"function"==typeof a&&!!a.call},Ma=function(a,b){if(!(2>arguments.length))for(var c=1,d=arguments.length;c<d;++c)a.push(arguments[c])},Na=function(a){var b=document;b.addEventListener?b.addEventListener("DOMContentLoaded",a,!1):b.attachEvent&&b.attachEvent("onDOMContentLoaded",a)},Oa=function(a){a.google_unique_id?++a.google_unique_id:a.google_unique_id=1},Pa=function(a){a=
a.google_unique_id;return"number"==typeof a?a:0},Qa=function(a){var b=a.length;if(0==b)return 0;for(var c=305419896,d=0;d<b;d++)c^=(c<<5)+(c>>2)+a.charCodeAt(d)&4294967295;return 0<c?c:4294967296+c},H=function(a,b){return b.getComputedStyle?b.getComputedStyle(a,null):a.currentStyle},Ra=/(^| )adsbygoogle($| )/;var Sa={overlays:1,interstitials:2};var Ta=!!window.google_async_iframe_id,Ua=function(a,b,c){var d=["<iframe"],f;for(f in a)a.hasOwnProperty(f)&&Ma(d,f+"="+a[f]);d.push('style="left:0;position:absolute;top:0;"');d.push("></iframe>");a=a.id;b="border:none;height:"+c+"px;margin:0;padding:0;position:relative;visibility:visible;width:"+b+"px;background-color:transparent";return['<ins id="',a+"_expand",'" style="display:inline-table;',b,'"><ins id="',a+"_anchor",'" style="display:block;',b,'">',d.join(" "),"</ins></ins>"].join("")};var Va=!0,Wa={},Za=function(a,b,c,d){var f=Xa,e,g=Va;try{e=b()}catch(h){try{var k=Ja(h);b="";h.fileName&&(b=h.fileName);var l=-1;h.lineNumber&&(l=h.lineNumber);g=f(a,k,b,l,c)}catch(m){try{var p=Ja(m);a="";m.fileName&&(a=m.fileName);c=-1;m.lineNumber&&(c=m.lineNumber);Xa("pAR",p,a,c,void 0,void 0)}catch(t){Ya({context:"mRE",msg:t.toString()+"\n"+(t.stack||"")},void 0)}}if(!g)throw h;}finally{if(d)try{d()}catch(v){}}return e},Xa=function(a,b,c,d,f,e){var g={};if(f)try{f(g)}catch(h){}g.context=a;g.msg=
b.substring(0,512);c&&(g.file=c);0<d&&(g.line=d.toString());g.url=Ka.URL.substring(0,512);g.ref=Ka.referrer.substring(0,512);$a(g);Ya(g,e);return Va},Ya=function(a,b){try{if(Math.random()<(b||.01)){var c="/pagead/gen_204?id=jserror"+ab(a),d="http"+("http:"==F.location.protocol?"":"s")+"://pagead2.googlesyndication.com"+c,d=d.substring(0,2E3);F.google_image_requests||(F.google_image_requests=[]);var f=F.document.createElement("img");f.src=d;F.google_image_requests.push(f)}}catch(e){}},$a=function(a){var b=
a||{};G(Wa,function(a,d){b[d]=F[a]})},bb=function(a,b){return function(){var c=arguments;return Za(a,function(){return b.apply(void 0,c)},void 0,void 0)}},cb=function(a,b){return bb(a,b)},db=function(a){return bb("aa:reactiveTag",a)},ab=function(a){var b="";G(a,function(a,d){if(0===a||a)b+="&"+d+"="+("function"==typeof encodeURIComponent?encodeURIComponent(a):escape(a))});return b};var eb=null,fb=function(){if(!eb){for(var a=window,b=a,c=0;a&&a!=a.parent;)if(a=a.parent,c++,Ha(a))b=a;else break;eb=b}return eb};var gb={google_ad_modifications:!0,google_analytics_domain_name:!0,google_analytics_uacct:!0},hb=function(a){a.google_page_url&&(a.google_page_url=String(a.google_page_url));var b=[];G(a,function(a,d){if(null!=a){var f;try{var e=[];ra(new pa,a,e);f=e.join("")}catch(g){}f&&(f=f.replace(/\\|\//,"\\$&"),Ma(b,d,"=",f,";"))}});return b.join("")};var ib=function(a){var b=arguments.length;if(1==b&&"array"==u(arguments[0]))return ib.apply(null,arguments[0]);for(var c={},d=0;d<b;d++)c[arguments[d]]=!0;return c};var jb={la:"google_auto_instream_debug",ma:"google_anchor_debug",na:"google_infinite_scroll_debug",oa:"google_inflate_debug",pa:"google_ia_debug",ra:"google_ia_debug_fi",ta:"google_ia_debug_spa",sa:"google_ia_debug_scr",qa:"google_ia_debug_allow_onclick",ua:"google_ladder_rung_debug",va:"google_lat_debug",wa:"google_lat_debug_all",xa:"google_resize_debug",za:"google_visible_intentful_click",ya:"google_supersize_debug"};var I=function(a){a=a.document;return("CSS1Compat"==a.compatMode?a.documentElement:a.body)||{}},lb=function(a){var b=!1;G(jb,function(c){kb(a,c)&&(b=!0)});return b},kb=function(a,b){if(!a||!a.indexOf)return!1;if(-1!=a.indexOf(b))return!0;var c=mb(b);return-1!=a.indexOf(c)?!0:!1},mb=function(a){var b="";G(a.split("_"),function(a){b+=a.substr(0,2)});return b};var J;a:{var nb=q.navigator;if(nb){var ob=nb.userAgent;if(ob){J=ob;break a}}J=""}var K=function(a){return-1!=J.indexOf(a)};var pb=function(){return K("iPad")||K("Android")&&!K("Mobile")||K("Silk")};var qb={"120x90":!0,"160x90":!0,"180x90":!0,"200x90":!0,"468x15":!0,"728x15":!0};var rb=/^([0-9.]+)px$/,sb=/^([0-9.]+)$/,L=function(a){return(a=rb.exec(a))?Number(a[1]):null},tb=function(a,b){for(var c=["width","height"],d=0;d<c.length;d++){var f="google_ad_"+c[d];if(!b.hasOwnProperty(f)){var e;e=(e=L(a[c[d]]))?Math.round(e):null;null!=e&&(b[f]=e)}}},ub=function(a,b){var c=b.document.documentElement;try{var d=c.getBoundingClientRect();return a.getBoundingClientRect().top-d.top}catch(f){return 0}};var vb={rectangle:1,horizontal:2,vertical:4},wb=[{width:970,height:90,format:2},{width:728,height:90,format:2},{width:468,height:60,format:2},{width:336,height:280,format:1},{width:320,height:100,format:2},{width:320,height:50,format:2},{width:300,height:600,format:4},{width:300,height:250,format:1},{width:250,height:250,format:1},{width:234,height:60,format:2},{width:200,height:200,format:1},{width:180,height:150,format:1},{width:160,height:600,format:4},{width:125,height:125,format:1},{width:120,
height:600,format:4},{width:120,height:240,format:4}];var xb=function(a,b){return b.width-a.width||b.height-a.height};var yb=Array.prototype,zb=yb.forEach?function(a,b,c){yb.forEach.call(a,b,c)}:function(a,b,c){for(var d=a.length,f="string"==typeof a?a.split(""):a,e=0;e<d;e++)e in f&&b.call(c,f[e],e,a)};var Ab=ib("area base br col command embed hr img input keygen link meta param source track wbr".split(" "));var M=function(){this.I="";this.W=Bb};M.prototype.n=!0;M.prototype.l=function(){return this.I};M.prototype.toString=function(){return"Const{"+this.I+"}"};var Cb=function(a){return a instanceof M&&a.constructor===M&&a.W===Bb?a.I:"type_error:Const"},Bb={};var N=function(){this.G="";this.U=Db};N.prototype.n=!0;var Db={};N.prototype.l=function(){return this.G};N.prototype.A=function(a){this.G=a;return this};var Eb=(new N).A(""),Fb=/^[-,."'%_!# a-zA-Z0-9]+$/;var O=function(){this.o="";this.V=Gb};O.prototype.n=!0;O.prototype.l=function(){return this.o};O.prototype.F=!0;O.prototype.r=function(){return 1};var Gb={};var P=function(){this.P="";this.X=Hb};P.prototype.n=!0;P.prototype.l=function(){return this.P};P.prototype.F=!0;P.prototype.r=function(){return 1};var Hb={};var Q=function(){this.o="";this.T=Ib;this.M=null};Q.prototype.F=!0;Q.prototype.r=function(){return this.M};Q.prototype.n=!0;Q.prototype.l=function(){return this.o};
var Jb=function(a){return a instanceof Q&&a.constructor===Q&&a.T===Ib?a.o:"type_error:SafeHtml"},Kb=/^[a-zA-Z0-9-]+$/,Lb={action:!0,cite:!0,data:!0,formaction:!0,href:!0,manifest:!0,poster:!0,src:!0},Mb={EMBED:!0,IFRAME:!0,LINK:!0,OBJECT:!0,SCRIPT:!0,STYLE:!0,TEMPLATE:!0},Nb=function(a){var b=0,c="",d=function(a){if("array"==u(a))zb(a,d);else{if(!(a instanceof Q)){var e=null;a.F&&(e=a.r());a=R(Ca(a.n?a.l():String(a)),e)}c+=Jb(a);a=a.r();0==b?b=a:0!=a&&b!=a&&(b=null)}};zb(arguments,d);return R(c,b)},
Ib={},R=function(a,b){return(new Q).A(a,b)};Q.prototype.A=function(a,b){this.o=a;this.M=b;return this};R("<!DOCTYPE html>",0);R("",0);var S=function(){return K("Edge")};var Ob=K("Opera")||K("OPR"),T=K("Edge")||K("Trident")||K("MSIE"),U=K("Gecko")&&!(-1!=J.toLowerCase().indexOf("webkit")&&!S())&&!(K("Trident")||K("MSIE"))&&!S(),Pb=-1!=J.toLowerCase().indexOf("webkit")&&!S(),Qb=function(){var a=J;if(U)return/rv\:([^\);]+)(\)|;)/.exec(a);if(T&&S())return/Edge\/([\d\.]+)/.exec(a);if(T)return/\b(?:MSIE|rv)[: ]([^\);]+)(\)|;)/.exec(a);if(Pb)return/WebKit\/(\S+)/.exec(a)},Rb=function(){var a=q.document;return a?a.documentMode:void 0},Sb=function(){if(Ob&&q.opera){var a=
q.opera.version;return"function"==u(a)?a():a}var a="",b=Qb();b&&(a=b?b[1]:"");return T&&!S()&&(b=Rb(),b>parseFloat(a))?String(b):a}(),Tb={},Ub=function(a){var b;if(!(b=Tb[a])){b=0;for(var c=ua(String(Sb)).split("."),d=ua(String(a)).split("."),f=Math.max(c.length,d.length),e=0;0==b&&e<f;e++){var g=c[e]||"",h=d[e]||"",k=RegExp("(\\d*)(\\D*)","g"),l=RegExp("(\\d*)(\\D*)","g");do{var m=k.exec(g)||["","",""],p=l.exec(h)||["","",""];if(0==m[0].length&&0==p[0].length)break;b=Ea(0==m[1].length?0:parseInt(m[1],
10),0==p[1].length?0:parseInt(p[1],10))||Ea(0==m[2].length,0==p[2].length)||Ea(m[2],p[2])}while(0==b)}b=Tb[a]=0<=b}return b},Vb=q.document,Wb=Rb(),Xb=!Vb||!T||!Wb&&S()?void 0:Wb||("CSS1Compat"==Vb.compatMode?parseInt(Sb,10):5);var Yb;if(!(Yb=!U&&!T)){var Zb;if(Zb=T)Zb=T&&(S()||9<=Xb);Yb=Zb}Yb||U&&Ub("1.9.1");T&&Ub("9");var $b={};var ac=function(a){var b=!1,c;return function(){b||(c=a(),b=!0);return c}}(function(){if(T)return Ub("10.0");var a=document.createElement("DIV"),b=Pb?"-webkit":U?"-moz":T?"-ms":Ob?"-o":null,c={transition:"opacity 1s linear"};b&&(c[b+"-transition"]="opacity 1s linear");b={style:c};if(!Kb.test("div"))throw Error("Invalid tag name <div>.");if("DIV"in Mb)throw Error("Tag name <div> is not allowed for SafeHtml.");var c=null,d="<div";if(b)for(var f in b){if(!Kb.test(f))throw Error('Invalid attribute name "'+
f+'".');var e=b[f];if(null!=e){var g;g=f;if(e instanceof M)e=Cb(e);else if("style"==g.toLowerCase()){if(!aa(e))throw Error('The "style" attribute requires goog.html.SafeStyle or map of style properties, '+typeof e+" given: "+e);if(!(e instanceof N)){var h="",k=void 0;for(k in e){if(!/^[-_a-zA-Z0-9]+$/.test(k))throw Error("Name allows only [-_a-zA-Z0-9], got: "+k);var l=e[k];if(null!=l){if(l instanceof M)l=Cb(l);else if(Fb.test(l)){for(var m=!0,p=!0,t=0;t<l.length;t++){var v=l.charAt(t);"'"==v&&p?
m=!m:'"'==v&&m&&(p=!p)}m&&p||(l="zClosurez")}else l="zClosurez";h+=k+":"+l+";"}}e=h?(new N).A(h):Eb}h=void 0;h=e instanceof N&&e.constructor===N&&e.U===Db?e.G:"type_error:SafeStyle";e=h}else{if(/^on/i.test(g))throw Error('Attribute "'+g+'" requires goog.string.Const value, "'+e+'" given.');if(g.toLowerCase()in Lb)if(e instanceof P)e=e instanceof P&&e.constructor===P&&e.X===Hb?e.P:"type_error:TrustedResourceUrl";else if(e instanceof O)e=e instanceof O&&e.constructor===O&&e.V===Gb?e.o:"type_error:SafeUrl";
else throw Error('Attribute "'+g+'" on tag "div" requires goog.html.SafeUrl or goog.string.Const value, "'+e+'" given.');}e.n&&(e=e.l());g=g+'="'+Ca(String(e))+'"';d+=" "+g}}f=void 0;null!=f?"array"==u(f)||(f=[f]):f=[];!0===Ab.div?d+=">":(c=Nb(f),d+=">"+Jb(c)+"</div>",c=c.r());(b=b&&b.dir)&&(c=/^(ltr|rtl|auto)$/i.test(b)?0:null);b=R(d,c);a.innerHTML=Jb(b);a=a.firstChild;b=a.style[Fa()];"undefined"!==typeof b?a=b:(b=a.style,c=$b.transition,c||(c=f=Fa(),void 0===a.style[f]&&(f=(Pb?"Webkit":U?"Moz":
T?"ms":Ob?"O":null)+Ga(f),void 0!==a.style[f]&&(c=f)),$b.transition=c),a=b[c]||"");return""!=a});var bc=function(a,b){this.u=["",""];this.i=a||"";this.w=b||""},V=function(a,b,c){0>a.u[b].indexOf(c)&&(a.u[b]+=c)},W=function(a,b){0>a.i.indexOf(b)&&(a.i=b+a.i)},cc=function(a,b){0>a.w.indexOf(b)&&(a.w=b+a.w)};bc.prototype.toString=function(){return[this.u[0],this.u[1],this.i,this.w].join("|")};
var dc=function(a){var b={da:0,ca:0,Z:!0};this.Y=null;this.K=a;var c=a.ownerDocument;this.L=c.defaultView||c.parentWindow;this.v=null;try{this.v=a.getBoundingClientRect()}catch(d){}var c=function(a){return a||0==a?+a:null},f=c(b.width);this.q=f;this.m=a=c(b.height);var e=c(b.da);this.t=f==e?null:e;c=c(b.ca);this.s=a==c?null:c;this.N=!!b.Z;this.D=!!b.Aa&&ac();this.i=new bc;this.p=null},hc=function(a){var b=a.L;a.p=function(){};ec(a,a.K,b);var c=a.K.parentElement;if(c){for(;c;){try{var d=/^head$/i.test(c.nodeName)?
null:H(c,b)}catch(f){cc(a.i,"c")}fc(a,b,c,d);if(d)if("none"==d.display){W(a.i,"n");break}else if("absolute"==d.position){W(a.i,"a");break}else if("fixed"==d.position){W(a.i,"f");break}else if("hidden"==d.visibility||"collapse"==d.visibility){W(a.i,"v");break}else"hidden"==d.overflow&&W(a.i,"o");c=c.parentElement;if(!c)try{var c=b.frameElement,e=b.parent;e&&e!=b&&(b=e)}catch(g){W(a.i,"c");break}}a.D&&gc(a)}},ic=function(a,b,c){if(3!=b.nodeType&&1==b.nodeType){if(/^(head|script|style)$/i.test(b.nodeName))return 0;
try{var d=H(b,c)}catch(f){}if(d){if("none"==d.display||"fixed"==d.position)return 0;if("absolute"==d.position){if(!a.v)return 0;c=null;try{c=b.getBoundingClientRect()}catch(e){return 0}return(c.right>a.v.left?2:0)|(c.bottom>a.v.top?4:0)}}return 1}return 0},ec=function(a,b,c){var d=0;if(!b||!b.parentElement)return!0;for(var f=!1,e=0,g=b.parentElement.childNodes,h=0;h<g.length;h++){var k=g[h];k==b?f=!0:(k=ic(a,k,c),d|=k,f&&(e|=k))}e&1&&(d&2&&V(a.i,0,"o"),d&4&&V(a.i,1,"o"));return!(d&1)},jc=function(a,
b,c,d,f,e,g,h){if(null!=g&&null!=h){if("string"==typeof e){if("100%"==e)return;e=E(e);null==e&&(cc(a.i,"n"),V(a.i,b,"d"))}if(null!=e)if(c){if(a.N){var k=Math.max(e+h-g,0);if(a.D){var l=a.p;a.p=function(a,c){a==b&&d.setAttribute(f,k-c);l(a,c)}}else d.setAttribute(f,k)}}else V(a.i,b,"d")}},kc=function(a){return!a||/^(auto|none|100%)$/.test(a)},lc=function(a){return!a||/^(0px|auto|none|0%)$/.test(a)},X=function(a,b,c,d,f,e,g,h,k){if(null!=h&&null!=k){if("string"==typeof g){if("m"==c?lc(g):kc(g))return;
g=L(g);null==g&&(cc(a.i,"p"),V(a.i,b,c))}if(null!=g)if(d&&f){if(a.N){var l=Math.max(g+k-h,0);if(a.D){var m=a.p;a.p=function(a,c){a==b&&(f[e]=l-c+"px");m(a,c)}}else f[e]=l+"px"}}else V(a.i,b,c)}},fc=function(a,b,c,d){try{var f=c.style}catch(e){cc(a.i,"s")}var g=c.getAttribute("width"),h=E(g),k=c.getAttribute("height"),l=E(k),m=ec(a,c,b),p=(b=f?f.width:null)?L(b):null,t=f?f.height:null,v=t?L(t):null,h=null!==p&&a.q>=p||null!==h&&a.q>=h,l=null!==v&&a.m>=v||null!==l&&a.m>=l,l=m||l||!(g||b||d&&(!lc(d.minWidth)||
!kc(d.maxWidth)));d=m||h||!(k||t||d&&(!lc(d.minHeight)||!kc(d.maxHeight)));jc(a,0,l,c,"width",g,a.q,a.t);jc(a,1,d,c,"height",k,a.m,a.s);X(a,0,"d",l,f,"width",b,a.q,a.t);X(a,1,"d",d,f,"height",t,a.m,a.s);X(a,0,"m",l,f,"minWidth",f&&f.minWidth,a.q,a.t);X(a,1,"m",d,f,"minHeight",f&&f.minHeight,a.m,a.s);X(a,0,"M",l,f,"maxWidth",f&&f.maxWidth,a.q,a.t);X(a,1,"M",d,f,"maxHeight",f&&f.maxHeight,a.m,a.s)},gc=function(a){var b=31.25,c=a.L,d=a.Y,f=a.t,e=a.s,g=a.p,h,k=function(){if(0<b){var a=H(d,c),k=L(a.width),
a=L(a.height);null!==k&&null!==f&&g(0,f-k);null!==a&&null!==e&&g(1,e-a)}else F.clearInterval(h),g(0,0),g(1,0);--b};F.setTimeout(function(){h=F.setInterval(k,16)},990)};var mc=function(a,b,c){if(!a)return null;for(var d=0;d<a.length;++d)if((a[d].ad_slot||b)==b&&(a[d].ad_tag_origin||c)==c)return a[d];return null};Va=!na;Wa={client:"google_ad_client",format:"google_ad_format",slotname:"google_ad_slot",output:"google_ad_output",ad_type:"google_ad_type",async_oa:"google_async_for_oa_experiment",dimpr:"google_always_use_delayed_impressions_experiment",peri:"google_top_experiment",pse:"google_pstate_expt"};var nc=function(a,b,c){c||(c=oa?"https":"http");return[c,"://",a,b].join("")};var oc=null;var pc=function(a){this.k=a;a.google_iframe_oncopy||(a.google_iframe_oncopy={handlers:{},upd:w(this.ja,this)});this.ga=a.google_iframe_oncopy},qc=Ca("var i=this.id,s=window.google_iframe_oncopy,H=s&&s.handlers,h=H&&H[i],w=this.contentWindow,d;try{d=w.document}catch(e){}if(h&&d&&(!d.body||!d.body.firstChild)){if(h.call){setTimeout(h,0)}else if(h.match){try{h=s.upd(h,i)}catch(e){}w.location.replace(h)}}");
pc.prototype.set=function(a,b){this.ga.handlers[a]=b;this.k.addEventListener&&this.k.addEventListener("load",w(this.aa,this,a),!1)};pc.prototype.aa=function(a){a=this.k.document.getElementById(a);try{var b=a.contentWindow.document;if(a.onload&&b&&(!b.body||!b.body.firstChild))a.onload()}catch(c){}};
pc.prototype.ja=function(a,b){var c=rc("rx",a),d;a:{if(a&&(d=a.match("dt=([^&]+)"))&&2==d.length){d=d[1];break a}d=""}d=(new Date).getTime()-d;c=c.replace(/&dtd=(\d+|M)/,"&dtd="+(1E4>d?d+"":"M"));this.set(b,c);return c};var rc=function(a,b){var c=new RegExp("\\b"+a+"=(\\d+)"),d=c.exec(b);d&&(b=b.replace(c,a+"="+(+d[1]+1||1)));return b};var sc=function(a){if(!a)return"";(a=a.toLowerCase())&&"ca-"!=a.substring(0,3)&&(a="ca-"+a);return a};var Y,Z=function(a){this.C=[];this.k=a||window;this.j=0;this.B=null;this.S=0},tc=function(a,b){this.ba=a;this.ka=b};Z.prototype.$=function(a,b){0!=this.j||0!=this.C.length||b&&b!=window?this.O(a,b):(this.j=2,this.R(new tc(a,window)))};Z.prototype.O=function(a,b){this.C.push(new tc(a,b||this.k));uc(this)};Z.prototype.ea=function(a){this.j=1;if(a){var b=cb("sjr::timeout",w(this.Q,this,!0));this.B=this.k.setTimeout(b,a)}};
Z.prototype.Q=function(a){a&&++this.S;1==this.j&&(null!=this.B&&(this.k.clearTimeout(this.B),this.B=null),this.j=0);uc(this)};Z.prototype.fa=function(){return!(!window||!Array)};Z.prototype.ha=function(){return this.S};Z.prototype.nq=Z.prototype.$;Z.prototype.nqa=Z.prototype.O;Z.prototype.al=Z.prototype.ea;Z.prototype.rl=Z.prototype.Q;Z.prototype.sz=Z.prototype.fa;Z.prototype.tc=Z.prototype.ha;var uc=function(a){var b=cb("sjr::tryrun",w(a.ia,a));a.k.setTimeout(b,0)};
Z.prototype.ia=function(){if(0==this.j&&this.C.length){var a=this.C.shift();this.j=2;var b=cb("sjr::run",w(this.R,this,a));a.ka.setTimeout(b,0);uc(this)}};Z.prototype.R=function(a){this.j=0;a.ba()};
var vc=function(a){try{return a.sz()}catch(b){return!1}},wc=function(a){return!!a&&("object"==typeof a||"function"==typeof a)&&vc(a)&&La(a.nq)&&La(a.nqa)&&La(a.al)&&La(a.rl)},xc=function(){if(Y&&vc(Y))return Y;var a=fb(),b=a.google_jobrunner;return wc(b)?Y=b:a.google_jobrunner=Y=new Z(a)},yc=function(a,b){xc().nq(a,b)},zc=function(a,b){xc().nqa(a,b)};var Ac=Ta?1==Pa(F):!Pa(F),Bc=function(){var a=B("script"),b;b=ga("","pagead2.googlesyndication.com");return["<",a,' src="',nc(b,"/pagead/js/r20150414/r20150409/show_ads_impl.js",""),'"></',a,">"].join("")},Cc=function(a,b,c,d){return function(){var f=!1;d&&xc().al(3E4);var e=a.document.getElementById(b);e&&!Ha(e.contentWindow)&&
3==a.google_top_js_status&&(a.google_top_js_status=6);try{if(Ha(a.document.getElementById(b).contentWindow)){var g=a.document.getElementById(b).contentWindow,h=g.document;h.body&&h.body.firstChild||(h.open(),g.google_async_iframe_close=!0,h.write(c))}else{var k=a.document.getElementById(b).contentWindow,l;e=c;e=String(e);if(e.quote)l=e.quote();else{g=['"'];for(h=0;h<e.length;h++){var m=e.charAt(h),p=m.charCodeAt(0),t=h+1,v;if(!(v=Da[m])){var x;if(31<p&&127>p)x=m;else{var n=m;if(n in A)x=A[n];else if(n in
Da)x=A[n]=Da[n];else{var z=n,r=n.charCodeAt(0);if(31<r&&127>r)z=n;else{if(256>r){if(z="\\x",16>r||256<r)z+="0"}else z="\\u",4096>r&&(z+="0");z+=r.toString(16).toUpperCase()}x=A[n]=z}}v=x}g[t]=v}g.push('"');l=g.join("")}k.location.replace("javascript:"+l)}f=!0}catch(C){k=fb().google_jobrunner,wc(k)&&k.rl()}f&&(f=rc("google_async_rrc",c),(new pc(a)).set(b,Cc(a,b,f,!1)))}},Dc=function(a){var b=["<iframe"];G(a,function(a,d){null!=a&&b.push(" "+d+'="'+a+'"')});b.push("></iframe>");return b.join("")},Fc=
function(a,b,c){Ec(a,b,c,function(a,b,e){a=a.document;for(var g=b.id,h=0;!g||a.getElementById(g);)g="aswift_"+h++;b.id=g;b.name=g;g=Number(e.google_ad_width);h=Number(e.google_ad_height);16==e.google_reactive_ad_format?(e=a.createElement("div"),e.innerHTML=Ua(b,g,h),c.appendChild(e.firstChild)):c.innerHTML=Ua(b,g,h);return b.id})},Ec=function(a,b,c,d){var f=B("script"),e={},g=b.google_ad_height;e.width='"'+b.google_ad_width+'"';e.height='"'+g+'"';e.frameborder='"0"';e.marginwidth='"0"';e.marginheight=
'"0"';e.vspace='"0"';e.hspace='"0"';e.allowtransparency='"true"';e.scrolling='"no"';e.allowfullscreen='"true"';e.onload='"'+qc+'"';d=d(a,e,b);var e=Gc(b)?D(["c","e"],la):null,h=b.google_ad_output,g=b.google_ad_format;g||"html"!=h&&null!=h||(g=b.google_ad_width+"x"+b.google_ad_height,"e"==e&&(g+="_as"));h=!b.google_ad_slot||Gc(b);g=g&&h?g.toLowerCase():"";b.google_ad_format=g;for(var g=[b.google_ad_slot,b.google_ad_format,b.google_ad_type,b.google_ad_width,b.google_ad_height],h=[],k=0,l=c;l&&25>k;l=
l.parentNode,++k)h.push(9!=l.nodeType&&l.id||"");(h=h.join())&&g.push(h);b.google_ad_unit_key=Qa(g.join(":")).toString();g=a.google_adk2_experiment=a.google_adk2_experiment||D(["C","E"],ka)||"N";if("E"==g){g=[];for(h=0;c&&25>h;++h){k=(k=9!=c.nodeType&&c.id)?"/"+k:"";a:{if(c&&c.nodeName&&c.parentElement)for(var l=c.nodeName.toString().toLowerCase(),m=c.parentElement.childNodes,p=0,t=0;t<m.length;++t){var v=m[t];if(v.nodeName&&v.nodeName.toString().toLowerCase()==l){if(c==v){l="."+p;break a}++p}}l=
""}g.push((c.nodeName&&c.nodeName.toString().toLowerCase())+k+l);c=c.parentElement}c=g.join()+":";g=a;h=[];if(g)try{for(var x=g.parent,k=0;x&&x!=g&&25>k;++k){for(var n=x.frames,l=0;l<n.length;++l)if(g==n[l]){h.push(l);break}g=x;x=g.parent}}catch(z){}b.google_ad_unit_key_2=Qa(c+h.join()).toString()}else"C"==g&&(b.google_ad_unit_key_2="ctrl");var x=hb(b),r;b=b.google_ad_client;if(n=Ac){if(!oc)b:{c=[F.top];n=[];for(g=0;h=c[g++];){n.push(h);try{if(h.frames)for(var C=h.frames.length,k=0;k<C&&1024>c.length;++k)c.push(h.frames[k])}catch(Vc){}}for(C=
0;C<n.length;C++)try{if(r=n[C].frames.google_esf){oc=r;break b}}catch(Wc){}oc=null}n=!oc}n?(r={style:"display:none"},r["data-ad-client"]=sc(b),r.id="google_esf",r.name="google_esf",r.src=nc(ga("","googleads.g.doubleclick.net"),"/pagead/html/r20150414/r20150409/zrt_lookup.html"),r=Dc(r)):r="";C=(new Date).getTime();b=a.google_top_experiment;if(n=a.google_async_for_oa_experiment)a.google_async_for_oa_experiment=
void 0;c=a.google_always_use_delayed_impressions_experiment;e=["<!doctype html><html><body>",r,"<",f,">",x,"google_show_ads_impl=true;google_unique_id=",a.google_unique_id,';google_async_iframe_id="',d,'";google_start_time=',da,";",b?'google_top_experiment="'+b+'";':"",n?'google_async_for_oa_experiment="'+n+'";':"",c?'google_always_use_delayed_impressions_experiment="'+c+'";':"",e?'google_append_as_for_format_override="'+e+'";':"","google_bpp=",C>da?C-da:1,";google_async_rrc=0;</",f,">",Bc(),"</body></html>"].join("");
(a.document.getElementById(d)?yc:zc)(Cc(a,d,e,!0))},Hc=Math.floor(1E6*Math.random()),Ic=function(a){var b;try{b={};for(var c=a.data.split("\n"),d=0;d<c.length;d++){var f=c[d].indexOf("=");-1!=f&&(b[c[d].substr(0,f)]=c[d].substr(f+1))}}catch(e){}c=b[3];if(b[1]==Hc&&(window.google_top_js_status=4,a.source==top&&0==c.indexOf(a.origin)&&(window.google_top_values=b,window.google_top_js_status=5),window.google_top_js_callbacks)){for(a=0;a<window.google_top_js_callbacks.length;a++)window.google_top_js_callbacks[a]();
window.google_top_js_callbacks.length=0}},Gc=function(a){return a.google_override_format||!qb[a.google_ad_width+"x"+a.google_ad_height]&&"aa"==a.google_loader_used},Jc=function(a,b){var c=navigator;if(ma&&a&&b&&c){var d=a.document,c=d.createElement("script"),f=sc(b);c.async=!0;c.type="text/javascript";c.src=nc("pagead2.googlesyndication.com","/pub-config/"+f+".js");d=d.getElementsByTagName("script")[0];d.parentNode.insertBefore(c,d)}};var Kc=function(a){return Ra.test(a.className)&&"done"!=a.getAttribute("data-adsbygoogle-status")},Mc=function(a,b){var c=window;a.setAttribute("data-adsbygoogle-status","done");Lc(a,b,c)},Lc=function(a,b,c){Nc(a,b,c);if(!Oc(a,b,c)){Oa(c);1==Pa(c)&&Jc(c,b.google_ad_client);G(gb,function(a,d){b[d]=b[d]||c[d]});b.google_loader_used="aa";var d=b.google_ad_output;if(d&&"html"!=d)throw Error("No support for google_ad_output="+d);Za("aa::main",function(){Fc(c,b,a)})}},Oc=function(a,b,c){var d;var f=b.google_ad_slot;
d=c.google_ad_modifications;if(!d||mc(d.ad_whitelist,f,b.google_tag_origin))d=null;else{var e=d.space_collapsing||"none";d=(f=mc(d.ad_blacklist,f))?{J:!0,H:f.space_collapsing||e}:d.remove_ads_by_default?{J:!0,H:e}:null}if(d&&d.J){if("none"==d.H)return!0;null!==E(a.getAttribute("width"))&&a.setAttribute("width",0);null!==E(a.getAttribute("height"))&&a.setAttribute("height",0);a.style.width="0px";a.style.height="0px";"slot_and_pub"==d.H&&hc(new dc(a));return!0}return!(d=H(a,c))||"none"!=d.display||
"on"==b.google_adtest||0<b.google_reactive_ad_format||b.google_reactive_ads_config?!1:(c.document.createComment&&a.appendChild(c.document.createComment("No ad requested because of display:none on the adsbygoogle tag")),!0)},Nc=function(a,b,c){for(var d=a.attributes,f=d.length,e=0;e<f;e++){var g=d[e];if(/data-/.test(g.name)){var h=g.name.replace("data","google").replace(/-/g,"_");b.hasOwnProperty(h)||(g=g.value,"google_reactive_ad_format"==h&&(g=+g,g=isNaN(g)?null:g),null===g||(b[h]=g))}}lb(c.location.hash)&&
(b.google_adtest="on");if(b.google_enable_content_recommendations&&1==b.google_reactive_ad_format)b.google_ad_width=I(c).clientWidth,b.google_ad_height=50,a.style.display="none";else if(1==b.google_reactive_ad_format)b.google_ad_width=320,b.google_ad_height=50,a.style.display="none";else if(8==b.google_reactive_ad_format)b.google_ad_width=I(c).clientWidth||0,b.google_ad_height=I(c).clientHeight||0,a.style.display="none",kb(c.location.hash,"google_ia_debug_spa")&&(b.google_vignette_manual_trigger=
!0);else if(d=b.google_ad_format,"auto"==d||/^((^|,) *(horizontal|vertical|rectangle) *)+$/.test(d)){b.google_responsive_optimization_experiment=D(["MC","ME"],ja)||"-";var d=a.offsetWidth,f=b.google_ad_format,k;if("auto"==f)k=I(c).clientWidth,k=Math.min(1200,k),k=.25>=d/k?4:3;else{e=0;for(k in vb)-1!=f.indexOf(k)&&(e|=vb[k]);k=e}b&&(b.google_responsive_formats=k);a:{if(b&&"ME"==b.google_responsive_optimization_experiment){e=1+Pa(c);h=ub(a,c)/I(c).clientHeight;e=!pb()&&(K("iPod")||K("iPhone")||K("Android")||
K("IEMobile"))?1==e?.22>h?[7,8,3,12,6,14,4,1,10,11,13,0,2,15,5,9]:.7>h?[3,7,8,14,12,4,6,1,10,2,0,13,15,11,5,9]:[3,7,8,4,6,14,12,2,1,0,10,13,5,9,11,15]:2==e?1.18>h?[3,7,8,14,12,4,1,0,6,2,10,9,5,15,11,13]:3.04>h?[3,7,8,14,4,2,1,6,0,12,10,5,9,11,15,13]:[3,7,8,4,6,1,2,14,12,0,5,10,11,9,15,13]:2.3>h?[3,7,14,8,1,12,0,2,6,4,10,5,13,11,9,15]:5.6>h?[3,7,8,14,1,2,12,4,0,6,10,5,11,9,13,15]:[3,7,8,0,12,14,1,4,2,6,5,13,10,11,15,9]:pb()?1==e?.18>h?[3,7,8,12,6,1,14,0,4,10,2,5,13,15,9,11]:.49>h?[3,8,6,7,12,1,0,14,
2,10,4,5,13,9,11,15]:[3,8,7,6,1,12,0,2,14,4,10,5,9,13,15,11]:2==e?.7>h?[3,8,6,7,1,0,12,2,14,10,4,9,5,13,11,15]:1.58>h?[3,8,7,6,1,12,0,2,14,10,4,9,5,13,11,15]:[3,8,7,6,1,12,0,2,14,4,10,9,5,11,13,15]:1.03>h?[3,12,6,8,1,7,0,14,2,10,4,5,9,11,15,13]:2.55>h?[3,8,6,7,12,1,2,0,14,4,10,5,9,11,15,13]:[3,8,12,6,7,1,0,2,14,4,10,5,9,11,15,13]:1==e?.21>h?[3,12,7,6,1,8,0,4,2,10,14,11,5,15,9,13]:.54>h?[3,7,6,1,12,8,2,0,4,10,14,9,5,11,15,13]:[3,7,1,6,12,2,0,8,4,10,14,5,9,11,15,13]:2==e?.6>h?[3,7,1,12,6,0,2,8,4,10,
14,9,5,11,13,15]:1.53>h?[3,7,1,6,12,2,0,8,4,10,14,5,9,11,13,15]:[3,7,1,6,12,2,0,8,4,10,14,5,9,11,15,13]:.74>h?[3,7,12,6,1,2,8,0,4,14,10,9,13,5,11,15]:1.95>h?[3,7,6,12,1,2,8,0,4,10,14,5,9,11,13,15]:[3,7,6,12,1,2,8,0,4,14,10,5,9,11,15,13];h=[];for(g=0;g<e.length;++g)h.push(wb[e[g]]);e=h}else e=wb.slice(0).sort(xb);if(g=h=488>I(c).clientWidth)g=Math.min(I(c).clientHeight,16*I(c).clientWidth/9),g=ub(a,c)<g-100;c=g;for(g=0;g<e.length;g++){var l=e[g];if(l.width<=d&&l.format&k&&!(320==l.width&&(h&&50==l.height||
!h&&100==l.height)||c&&250<=l.height)){c=l;break a}}c=null}if(!c)throw Error("Cannot find a responsive size for a container of width="+d+"px and data-ad-format="+f);b.google_ad_width=300<d&&300<c.height?c.width:1200<d?1200:Math.round(d);b.google_ad_height=c.height;a.style.height=c.height+"px";b.google_ad_resizable=!0;delete b.google_ad_format;b.google_loader_features_used=128}else if(!sb.test(b.google_ad_width)&&!rb.test(a.style.width)||!sb.test(b.google_ad_height)&&!rb.test(a.style.height)?(d=H(a,
c),a.style.width=d.width,a.style.height=d.height,tb(d,b),b.google_loader_features_used=256):(tb(a.style,b),b.google_ad_output&&"html"!=b.google_ad_output||300!=b.google_ad_width||250!=b.google_ad_height||(d=I(c).clientHeight,ub(a,c)>1.5*d&&(d=a.style.width,a.style.width="100%",f=a.offsetWidth,a.style.width=d,b.google_available_width=f))),f=b.google_ad_width,d=b.google_ad_height,f&&d&&!qb[f+"x"+d]&&(d=D("CD ED CA EA CW EW".split(" "),ia)))"CD"==d?b.google_overflowing_ads_experiment=d:((f=/W$/.test(d)&&
728>f)||(f=/^E/.test(d),k=I(c),a&&a.getBoundingClientRect&&k&&k.getBoundingClientRect?(c=a.getBoundingClientRect(),k=k.getBoundingClientRect(),c=Math.min(c.right,k.right)-Math.max(c.left,k.left),c=Math.round(Math.max(0,c))):c=0,160>c||15>b.google_ad_width-c?a=!1:(k=a.style.width||"",a.style.width="100%",e=a.offsetWidth,160>e||0>c-e?(a.style.width=k,a=!1):(f?(b.google_ad_width=c,a.style.width=c+"px"):a.style.width=k,a=!0)),f=!a&&"ED"!=d),f||(b.google_overflowing_ads_experiment=d));0<b.google_reactive_ad_format&&
!b.google_pgb_reactive&&(b.google_pgb_reactive=3)},Pc=function(a){for(var b=document.getElementsByTagName("ins"),c=0,d=b[c];c<b.length;d=b[++c])if(Kc(d)&&(!a||d.id==a))return d;return null},Qc=!1,Rc=function(a){var b={};G(Sa,function(c,f){a.hasOwnProperty(f)&&(b[f]=a[f])});aa(a.enable_page_level_ads)&&(b.page_level_pubvars=a.enable_page_level_ads);var c=document.createElement("ins");c.className="adsbygoogle";c.style.display="none";document.body.appendChild(c);Mc(c,{google_reactive_ads_config:b,google_ad_client:a.google_ad_client})},
Sc=function(a){if(Qc)throw Error("adsbygoogle.push(): Only one 'enable_page_level_ads'  allowed per page.");Qc=!0;document.body?Rc(a):Na(db(function(){Rc(a)}))},Tc=function(a){var b;a:{if(a.enable_page_level_ads){if("string"==typeof a.google_ad_client){b=!0;break a}throw Error("adsbygoogle.push(): 'google_ad_client' is missing from the tag config.");}b=!1}if(b)Sc(a);else{b=a.element;a=a.params||{};if(b){if(!Kc(b)&&(b=b.id&&Pc(b.id),!b))throw Error("adsbygoogle: 'element' has already been filled.");
if(!("innerHTML"in b))throw Error("adsbygoogle.push(): 'element' is not a good DOM element.");}else if(b=Pc(),!b)throw Error("adsbygoogle.push(): All ins elements in the DOM with class=adsbygoogle already have ads in them.");Mc(b,a)}},Uc=function(){if(!window.google_top_experiment&&!window.google_top_js_status){var a=window;if(2!==(a.top==a?0:Ha(a.top)?1:2))window.google_top_js_status=0;else if(top.postMessage){var b;try{b=F.top.frames.google_top_static_frame?!0:!1}catch(c){b=!1}if(b){if(window.google_top_experiment=
D(["jp_c","jp_zl","jp_wfpmr","jp_zlt","jp_wnt"],ha),"jp_c"!==window.google_top_experiment){a=window;a.addEventListener?a.addEventListener("message",Ic,!1):a.attachEvent&&a.attachEvent("onmessage",Ic);window.google_top_js_status=3;a={0:"google_loc_request",1:Hc};b=[];for(var d in a)b.push(d+"="+a[d]);top.postMessage(b.join("\n"),"*")}}else window.google_top_js_status=2}else window.google_top_js_status=1}if((d=window.adsbygoogle)&&d.shift)for(b=20;(a=d.shift())&&0<b--;)try{Tc(a)}catch(f){throw window.setTimeout(Uc,
0),f;}d&&d.loaded||(window.adsbygoogle={push:Tc,loaded:!0})};Uc();})();
