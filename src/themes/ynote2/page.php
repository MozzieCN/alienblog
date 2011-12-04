<?php $this->need('header.php'); ?>
<div id="container">
    	<div id="content">
            <div class="post">
				<div class="date"><span class="day"><?php $this->date('d'); ?></span></div>
				<h2><?php $this->title() ?></h2>
				<div class="pageinfo">
				</div>
				<div class="con">
					<?php $this->content(''); ?>
				</div>
				<div class="under">
					<p>本文地址：<a href="<?php $this->permalink() ?>"><?php $this->permalink() ?></a></p>
				</div>
			</div>
        </div>
		 <div class="sidebar">
		 <div id="menu">
    <ul>
		<li><a href="<?php $this->options->siteUrl(); ?>about">ABOUT</a></li>
		<li><a href="<?php $this->options->siteUrl(); ?>feed">FEED</a></li>
	</ul> 
</div>
			<div class="block form"> 
    <form action="/search" class="sidebar-box search" method="get">
    <input id="search-input" type="text" name="s" class="inputbox" value="输入以进行搜索" onfocus="if (this.value == '输入以进行搜索') this.value = ''" onblur="if (this.value == '') this.value = '输入以进行搜索'" />
</form>
</div> 
	
<div class="block">
	<h3><?php _e('最新文章'); ?></h3> 
    <ul>
				<?php $this->widget('Widget_Contents_Post_Recent')
                ->parse('<li><a href="{permalink}">{title}</a></li>'); ?>
	</ul> 
</div>
<div class="block postarch"><h3><?php _e('文章归档'); ?></h3> 
    <ul> 
		<?php $this->widget('Widget_Contents_Post_Date', 'type=month&format=M Y')
        ->parse('<li><a href="{permalink}">{date}</a></li>'); ?>
    </ul> 
</div> 
<div class="clear"></div> 
		</div>
    </div>
<?php $this->need('footer.php'); ?>