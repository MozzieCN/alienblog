<?php $this->need('header.php'); ?>
<div id="container">
    	<div id="content">
			<div class="place">
	<a href="<?php $this->options->siteUrl(); ?>">首页</a>  &gt; <?php $this->archiveTitle(' &gt; ','',''); ?> 
			</div>
        	<?php while($this->next()): ?>
            <div class="post">
				<div class="date"><span class="day"><?php $this->date('d'); ?></span></div>
				<h2><a href="<?php $this->permalink() ?>"><?php $this->title() ?></a></h2>
				<div class="info">
					<span class="time"><?php $this->date('M Y'); ?></span>
                    <span class="tags">TAGS: <?php $this->tags(',', true, 'none'); ?></span>
                    <span class="comments"><?php $this->commentsNum('NO COMMENTS', '1 COMMENT', '%d COMMENTS'); ?></span>
					<div class="clear"></div>
				</div>
				<div class="con"><div class="indexpage">
					<?php $this->content('阅读全文'); ?>
				</div></div>
			</div>
			 <?php endwhile; ?>	
			<div class="post"><?php $this->pageNav('上一页','下一页',10,'...');?></div>
        </div>
		 <div class="sidebar"> 
        <?php $this->need('sidebar.php'); ?>
		</div>
    </div>
<?php $this->need('footer.php'); ?>

