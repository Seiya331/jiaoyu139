{dede:noteinfo notename="公务员" channelid="1" macthtype="string"
    refurl="http://" sourcelang="utf-8" cosort="asc"
  isref="no" exptime="10" usemore="0" /}
{dede:listrule sourcetype="batch" rssurl="http://" regxurl="http://v.huatu.com/news/list/index.php?page=(*)"
startid="1" endid="3" addv="1" urlrule="area" musthas="news"
 nothas="" listpic="0" usemore="0"}
    {dede:addurls}{/dede:addurls}
    {dede:batchrule}{/dede:batchrule}
    {dede:regxrule}{/dede:regxrule}
    {dede:areastart}<ul class="listSty01 mt20">{/dede:areastart}
    {dede:areaend}<div class="pageNumber">{/dede:areaend}
{/dede:listrule}
