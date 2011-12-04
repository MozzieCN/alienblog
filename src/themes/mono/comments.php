<?php 
if (!defined('__TYPECHO_ROOT_DIR__')) {
    exit;
}
    function threadedComments($thiss, $singleCommentOptions)
    {
    $singleCommentOptions = Typecho_Config::factory($singleCommentOptions);
    $singleCommentOptions->setDefault(array(
        'before'        =>  '<ol class="comment-list">',
        'after'         =>  '</ol>',
        'beforeAuthor'  =>  '',
        'afterAuthor'   =>  '',
        'beforeDate'    =>  '',
        'afterDate'     =>  '',
        'dateFormat'    =>  $thiss->commentDateFormat,
        'replyWord'     =>  _t('回复'),
        'avatarSize'    =>  32,
        'defaultAvatar' =>  NULL
    ));
    ?>

<li id="<?php $thiss->theId(); ?>" class="comment<?php
    if ($thiss->authorId) echo ($thiss->authorId == $thiss->ownerId ? ' admin-comment' : ' user-comment');
    ?>">
  <div class="comment-meta">
    <div class="comment-meta-left">
      <?php $thiss->gravatar(48, NULL); //$singleCommentOptions->defaultAvatar); ?>
      <ul class="comment-name-date">
        <li class="comment-name"><span id="commentauthor-<?php $thiss->coid(); ?>">
          <?php $thiss->author(); ?>
          </span></li>
        <li class="comment-date">
          <?php $thiss->date($singleCommentOptions->commentDateFormat); ?>
        </li>
      </ul>
    </div>
    <ul class="comment-act">
    <?php if (!$thiss->isTopLevel){ ?>
      <li class="comment-reply">
        <?php $thiss->reply('REPLY'); ?>
      </li><?php }; /* ?>
      <li class="comment-quote"> <?php echo '<a onclick="MGJS_CMT.quote(\''. $thiss->coid . '\');" href="javascript:void(0);">QUOTE</a>'; ?> </li><?php */ ?>
    </ul>
  </div>
  <div class="comment-content">
    <?php $thiss->content(); ?>
  </div>
  <?php if ($thiss->children) { ?>
  <ul class="children">
    <?php $tmpsingleCommentOptions = $singleCommentOptions;
    $tmpsingleCommentOptions->before = '';
    $tmpsingleCommentOptions->after = '';
    $thiss->threadedComments($tmpsingleCommentOptions); ?>
  </ul>
  <?php } ?>
</li>
<?php
    }; ?>
<div id="comments">
  <div id="comment_header" class="clearfix">
    <ul id="comment_header_left">
      <li id="add_comment"><a href="#respond">Write comment</a></li>
      <li id="comment_feed"><a href="<?php $this->feedUrl(); ?>" title="Comments RSS">Comments RSS</a></li>
    </ul>
    <ul id="comment_header_right">
      <li id="pingback_switch"><a href="javascript:void(0);">Pingback ( 0 )</a></li>
      <li id="comment_switch" class="comment_switch_active"><a href="javascript:void(0);">
        <?php $this->commentsNum('No Comments Yet','Just One Comment',' %d Comments'); ?>
        </a></li>
    </ul>
  </div>
  <!-- comment_header END -->
  <div id="comment_area"> 
    <!-- start commnet -->
    <?php $this->comments('comment')->to($comments); ?>
    <?php if ($comments->have()): ?>
    <div class="page_navi clearfix">
      <?php $comments->pageNav(); ?>
    </div>
    <?php $comments->listComments(); ?>
    <div class="page_navi clearfix">
      <?php $comments->pageNav(); ?>
    </div>
    <?php else: ?>
    <ol class="comment-list">
      <li class="comment even_comment">
        <div class="comment-content">
          <p>No comments yet.</p>
        </div>
      </li>
    </ol>
    <?php endif; ?>
    <!-- comments END --> 
  </div>
  <!-- #commentlist END -->
  
  <div id="pingback_area"> 
    <!-- start pingback -->
    <div id="pingback_url_wrapper">
      <label for="pingback_url">Pingback URL</label>
      <input type="text" name="pingback_url" id="pingback_url" size="60" value="<?php $this->options->xmlRpcUrl(); ?>" readonly="readonly" onfocus="this.select()" />
    </div>
    <!-- pingback end --> 
  </div>
  <!-- #pingbacklist END -->
  <?php if($this->allow('comment')): ?>
  <div id="<?php $this->respondId(); ?>" class="respond">
    <fieldset class="comment_form_wrapper">
      <div id="cancel_comment_reply">
        <?php $comments->cancelReply('Click here to cancel reply.'); ?>
      </div>
      <form action="<?php $this->commentUrl(); ?>" method="post" id="commentform">
        <?php if($this->user->hasLogin()): ?>
        <div id="comment_user_login">
          <p>Logged in as <a href="<?php $this->options->profileUrl(); ?>">
            <?php $this->user->screenName(); ?>
            </a>. <a href="<?php $this->options->logoutUrl(); ?>" title="Logout">Logout
            &raquo;</a></p>
        </div>
        <?php else: ?>
        <div id="guest_info">
          <div id="guest_name">
            <label for="author"><span>NAME</span>( required )</label>
            <input type="text" name="author" id="author" value="<?php $this->remember('author'); ?>" size="22" tabindex="1" />
          </div>
          <div id="guest_email">
            <label for="email"><span>E-MAIL</span>
              <?php if ($this->options->commentsRequireMail): ?>
              ( required ) - will not be published -
              <?php endif; ?>
            </label>
            <input type="text" name="mail" id="email" value="<?php $this->remember('mail'); ?>" size="22" tabindex="2" />
          </div>
          <div id="guest_url">
            <label for="url"><span>URL</span>
              <?php if ($this->options->commentsRequireURL): ?>
              ( required )
              <?php endif; ?>
            </label>
            <input type="text" name="url" id="url" value="" size="22" tabindex="3" />
          </div>
        </div>
        <?php endif;  ?>
        <div class="allowed_tag">
          <pre style="white-space:nowrap; margin-top:12px;">You can use the following tags in the comments:<br /><br />
  <?php $this->options->commentsHTMLTagAllowed(); ?>
  </pre>
        </div>
        <div id="comment_textarea">
          <textarea name="text" id="comment" cols="50" rows="10" tabindex="4"><?php $this->remember('text'); ?></textarea>
        </div>
        <div id="submit_comment_wrapper">
          <input name="submit" type="submit" id="submit_comment" tabindex="5" value="Submit Comment (Ctrl+Enter)" title="Submit Comment" alt="Submit Comment" />
        </div>
        <?php /* <div id="input_hidden_field">
          <input type='hidden' name='comment_post_ID' value='55' id='comment_post_ID' />
          <input type='hidden' name='parent' id='comment_parent' value='0' />
        </div> */ ?>
      </form>
    </fieldset>
  </div>
  <!-- #comment-form-area END -->
  <?php else: ?>
  <ol class="comment-list">
    <li class="comment even_comment">
      <div class="comment-content">
        <p>Comment has been closed!</p>
      </div>
    </li>
  </ol>
  <?php endif; ?>
</div>
<!-- #comment end -->