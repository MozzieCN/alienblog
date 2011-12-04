<?php $this->need('header.php'); ?>
<div id="container">
    	<div id="content">
			<div class="place">
				首页 &gt; <?php $this->category(); ?>  &gt; <?php $this->title() ?>
			</div>
            <div class="post">
				<div class="date"><span class="day"><?php $this->date('d'); ?></span></div>
				<h2><?php $this->title() ?></h2>
				<div class="info">
					<span class="time"><?php $this->date('M Y'); ?></span>
                    <span class="tags">TAGS: <?php $this->tags(',', true, 'none'); ?></span>
                    <span class="comments"><?php $this->commentsNum('NO COMMENTS', '1 COMMENT', '%d COMMENTS'); ?></span>
					<div class="clear"></div>
				</div>
				<div class="con">
					<?php $this->content(''); ?>
				</div>
				<div class="under">
					<p>本文地址：<a href="<?php $this->permalink() ?>"><?php $this->permalink() ?></a></p>
				</div>
			</div>
			<div class="postunder">
			<?php $this->need('comments.php'); ?>
			</div>
        </div>
				<div class="sidebar"> 
        <?php $this->need('sidebar.php'); ?>
				</div>
</div>							
<?php $this->need('footer.php'); ?>