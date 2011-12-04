<div id="menu">
    <ul>
		<li><a href="{{_option('site_url')}}/about">ABOUT</a></li>
		<li><a href="{{_option('site_url')}}/feed">FEED</a></li>
	</ul> 
</div>
<div class="block form"> 
    <form action="/search" class="sidebar-box search" method="get">
    <input id="search-input" type="text" name="s" class="inputbox" value="输入以进行搜索" onfocus="if (this.value == '输入以进行搜索') this.value = ''" onblur="if (this.value == '') this.value = '输入以进行搜索'" />
</form>
</div> 
 		
<div class="block">
	<h3>最新文章</h3> 
    <ul>
	</ul> 
</div>
		
<div class="block comment"><h3><?php _e('最近回复'); ?></h3> 
    <ul>
	</ul> 
</div>

<div class="clear"></div> 
