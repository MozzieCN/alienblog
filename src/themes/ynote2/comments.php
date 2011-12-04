<div id="comments">
            <?php $this->comments()->to($comments); ?>

			<h4><?php $this->commentsNum(_t('当前无评论'), _t('仅有一条评论'), _t('已有 %d 条评论')); ?></h4>
            <?php $comments->pageNav(); ?> 
            <?php $comments->listComments(); ?>
            <?php if($this->allow('comment')): ?>
            <div id="<?php $this->respondId(); ?>" class="respond">
            
            <div class="cancel-comment-reply">
            <?php $comments->cancelReply(); ?>
            </div>
            <div class="addcomment"></div>
			<h4 id="response"><?php _e('添加新评论'); ?></h4>
			<form method="post" action="<?php $this->commentUrl() ?>" id="comment_form">
                <?php if($this->user->hasLogin()): ?>
				<p>Logged in as <a href="<?php $this->options->profileUrl(); ?>"><?php $this->user->screenName(); ?></a>. <a href="<?php $this->options->logoutUrl(); ?>" title="Logout"><?php _e('退出'); ?> &raquo;</a></p>
                <?php else: ?>
				<p>
                    <label for="author"><?php _e('昵称'); ?></label>
					<input type="text" name="author" id="author" class="text" size="15" value="<?php $this->remember('author'); ?>" />
				</p>
				<p>
                    <label for="mail"><?php _e('邮箱'); ?></label>
					<input type="text" name="mail" id="mail" class="text" size="15" value="<?php $this->remember('mail'); ?>" />
				</p>
				<p>
                    <label for="url"><?php _e('网站'); ?></label>
					<input type="text" name="url" id="url" class="text" size="15" value="<?php $this->remember('url'); ?>" />
				</p>
                <?php endif; ?>
				<p><label for="url"><?php _e('评论'); ?></label><textarea rows="5" cols="50" name="text" class="textarea"><?php $this->remember('text'); ?></textarea></p>
				<p><label for="url"><?php _e('　　'); ?></label><input type="submit" value="<?php _e('提交评论'); ?>" class="submit"/></p>
			</form>
            </div>
            <?php else: ?>
            <?php endif; ?>
		</div>
