#-*- coding:utf-8 -*-
class Global:
    project_dir = '/var/www/monkey/www/'
    static_dir = '/var/www/monkey/static/'

    _mod_header_html = u'''##-*- coding:utf-8 -*-
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title></title>
        ${cssfiles}
        ${jsfiles}
        <style type="text/css">
            *{margin:0;padding:0;}
            html{overflow-y:scroll;}
            .ma_modulelist{font-size:12px;list-style:none;}
            .ma_moduletitle{
                font-size:14px;
                color:#333;
                height:25px;
                border-style:solid dotted;
                border-width:1px;
                border-color:#ddd #888;
                line-height:25px;
                text-align:center;
                background:#f3f3f3;
                color:#333;
                position:relative;
            }
            .ma_moduletitle span.ma_author{
                position:absolute;
                left:0;
                top:0;
                width:180px;
                text-align:left;
                padding-left:0.5em;
            }
            .ma_modulecontent{
                padding:8px 0;
                margin-bottom:8px;
                border-style:none dotted dotted;
                border-width:1px;
                border-color:#888;
                border-radius:0 0 5px 5px;
                background:#fff;
                zoom:1;
            }
            #ma_out_mod_box{
                border-bottom:3px solid #3B5998;
                height:0;
                overflow:hidden;
                position:relative;
                padding-top:16px;
                background:#fff;
                width:100%;
                z-index:99999999;
            }
            #ma_control{
                position:absolute;
                bottom:0;
                _bottom:-1px;
                left:50%;
            }
            #ma_control div{
                position:relative;
                float:left;
                left:-50%;
                border-radius:3px 3px 0 0;
                background:#3B5998;
                color:#fff;
                font-size:14px;
                font-weight:bold;
                height:16px;
                line-height:17px;
                padding:0 8px;
                cursor:pointer;
                overflow:hidden;
                font-family:Tahoma;
            }
            #ma_content{
                overflow-x:hidden;
                overflow-y:scroll;
                padding-bottom:8px;
                position:relative;
            }
            #ma_htmlcode{
                position: absolute;
				z-index:99999999999;
				border:2px #3B5998 solid;
				border-radius:5px;
				top:21px;
				left:10%;
				width:80%;
				overflow-x:hidden;
				overflow-y:auto;
				background:#151515;
				color:#fff;
				resize:none;
				outline:none;
				border-shadow:0 0 2px #666 inset;
				font-size:12px;
				padding:0 10px;
            }
        </style>
    </head>

    <body>
            %if tpl == '_merge':
                <div id="ma_out_mod_box">
                    <div id="ma_content">${basehtml}</div>
                    <div id="ma_control"><div>Show the base moudles</div></div>
                </div>
                ${modhtml}
            %else:
                <div id="ma_out_mod_box">
                    <div id="ma_content">${basehtml}</div>
                    <div id="ma_control"><div>Show the base moudles</div></div>
                </div>
            %endif'''

    _mod_footer_html = u'''##-*- coding:utf-8 -*-
    </body>
    <script type="text/javascript">
        document.title = '${p} | ' + '${tpl}'.substring(1);
        var outModBox = document.getElementById("ma_out_mod_box");
        var oControl = document.getElementById("ma_control").getElementsByTagName('div')[0];
        var oMacontent = document.getElementById('ma_content');
        var html = document.documentElement;
        var oModList = document.getElementsByTagName("ul");
        var oAuthor = document.createElement('span');
        var htmlCode = document.getElementById("ma_htmlcode");
        var scrollPosition = 0;
        oAuthor.className = 'ma_author';
        for(var mitem = 0; mitem < oModList.length; mitem++){
            var modAuthor = "Author:" + (oModList[mitem].getAttribute("id") ? oModList[mitem].getAttribute("id") : '${tpl}'.substring(1));
            var mitemall = oModList[mitem].getElementsByTagName("div");
            for(var l = 0; l < mitemall.length; l++){
                if(mitemall[l].className == "ma_moduletitle"){
                    var s = oAuthor.cloneNode(true);
                    s.innerHTML = modAuthor;
                    mitemall[l].appendChild(s)    
                }            
            }
        }
        oMacontent.style.height = html.clientHeight - 11 + 'px';
        if('${p}' == 'base'){
            outModBox.style.display = 'none';    
        }
        oControl.onclick = function(){
           if(this.getAttribute('show') == 'yes'){
                this.setAttribute('show','no');
                outModBox.style.height = 0;
                outModBox.style.paddingTop = '16px';
                this.innerHTML = 'Show the base moudles';
                html.style.overflowY = 'scroll';
                document.documentElement.scrollTop = scrollPosition;
                document.body.scrollTop = scrollPosition;
           }else{
                this.setAttribute('show','yes');
                scrollPosition = (document.documentElement && document.documentElement.scrollTop) ? document.documentElement.scrollTop : document.body.scrollTop;
                document.documentElement.scrollTop = 0;
                document.body.scrollTop = 0;   
                outModBox.style.height = html.clientHeight - 3 + 'px';
                oMacontent.style.height = html.clientHeight - 11 + 'px';
                outModBox.style.paddingTop = 0;
                this.innerHTML = 'Hide the base moudles';
                html.style.overflowY = 'hidden';
                outModBox.style.position = 'relative';
                outModBox.style.top = 0;
        }}
        window.onresize = function(){
            if(oControl.getAttribute('show') == 'yes'){
                outModBox.style.height = html.clientHeight - 3 + 'px';
                oMacontent.style.height = html.clientHeight - 11 + 'px';
            }
            if(htmlCode && htmlCode.style.display == 'block'){
                htmlCode.style.height = document.documentElement.clientHeight - 46 + "px";
            }
        }
       window.onscroll = function(){
            var t = (document.documentElement && document.documentElement.scrollTop) ? document.documentElement.scrollTop : document.body.scrollTop;
            if(t > 16){
                outModBox.style.position = 'absolute';
                outModBox.style.top = t + 'px';
            }else{
                outModBox.style.position = 'relative';
                outModBox.style.top = 0;
            }
			if(htmlCode && htmlCode.style.display == 'block'){
				htmlCode.style.top = 21 + t + 'px';
			}
       }
       document.onclick = function(e){
            e = e || window.event;
            target = e.target || e.srcElement;
            var t = (document.documentElement && document.documentElement.scrollTop) ? document.documentElement.scrollTop : document.body.scrollTop;
            if(target.className == "ma_moduletitle"){
                if (!htmlCode){
                    htmlCode = document.createElement('textarea');
                    htmlCode.setAttribute('id','ma_htmlcode');
                    document.body.appendChild(htmlCode);
                }
                htmlCode.style.display = 'block';
				htmlCode.focus()
                htmlCode.style.height = document.documentElement.clientHeight - 46 + "px";
				htmlCode.value = next(target).innerHTML.replace(/>\s/ig,">\n").replace(/\s</ig,"\n<");
				document.documentElement.scrollTop = t;
				document.body.scrollTop = t;
            }else if(htmlCode && target.getAttribute("id") != 'ma_htmlcode'){
				htmlCode.style.display = "none";
			} 
 	   }
       function next(ele){
           ele = (typeof(ele) === 'string') ? document.getElementById(ele) : ele;
           do{
               ele = ele.nextSibling;        
           }while(ele.nodeType !== 1);
           return ele;
       }
       function stopProgagation(e){
           e = e || window.event;
           if(e.stopProgagation){
               e.stopProgagation();
           }else{
               e.cancelBubble = true;
           }
       }
       document.onkeydown = function(e){
            e = e || window.event;
            if(htmlCode && htmlCode.style.display == 'block' && e.keyCode == 27){
                htmlCode.style.display = 'none';
            }
       }
    </script>

</html>'''

    _mod_user_html = u'''##-*- coding:utf-8 -*-
<%include file='_header.html' />

<ul class="ma_modulelist">
    <li class="ma_moduleitem">
        <div class="ma_modulebox">
            <div class="ma_moduletitle">

            </div>
            <div class="ma_modulecontent">

            </div>
        </div>
    </li>
</ul>

<%include file='_footer.html' />'''

    _mod_merge_html = u'''##-*- coding:utf-8 -*-
<%include file='_header.html' />
<%include file='_footer.html' />'''

