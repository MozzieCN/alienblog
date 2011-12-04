<?php 
if (!defined('__TYPECHO_ROOT_DIR__')) {
    exit;
} ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head profile="http://gmpg.org/xfn/11">
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta http-equiv="X-UA-Compatible" content="IE=EmulateIE7" />
<title><?php $this->archiveTitle(' &raquo; ', '', ' - '); ?><?php $this->options->title(); ?></title>
<?php if($this->is('index')){ ?>
<meta name="description" content="<?php $this->options->description(); ?>" />
<?php } ?>

<?php $this->header('generator=Typecho&template=By CzBiX&description='); ?>
<link rel="stylesheet" href="<?php $this->options->themeUrl('style.css'); ?>" type="text/css" />
<link rel="stylesheet" href="<?php $this->options->themeUrl('comment-style.css'); ?>" type="text/css" />
<link rel="stylesheet" href="<?php $this->options->themeUrl('highslide/highslide.css'); ?>" type="text/css" media="screen" />
<!--[if lt IE 7]>
<link rel="stylesheet" href="<?php $this->options->themeUrl('ie6.css'); ?>" type="text/css" />
<![endif]-->
<style type="text/css">
.post img, .post a img {
	border:1px solid #ccc;
	padding:5px;
	margin:0 10px 0 0;
	background:#f2f2f2;
}
.post a:hover img {
	border:1px solid #38a1e5;
	background:#9cd1e1;
}
.post img.wp-smiley {
	border:0px;
	padding:0px;
	margin:0px;
	background:none;
}
</style>
</head>

<body>
<div id="loading">Loading...</div>
<div id="wrapper">
<div id="header">
  <div id="header_top">
    <div id="logo"><a href="<?php $this->options->siteUrl(); ?>"><?php if ($this->options->logoUrl){ ?>
        <img src="<?php $this->options->logoUrl() ?>" alt="<?php $this->options->title(); ?>" />
        <?php } else { 
          $this->options->title();
          }; ?>
      </a>
      <h1>
        <?php $this->options->description() ?>
      </h1>
    </div>
    <div class="header_menu">
      <ul class="menu">
        <li<?php if($this->is('index')): ?> class="current_page_item"<?php endif; ?>><a href="<?php $this->options->siteUrl(); ?>">
          <?php _e('HOME'); ?>
          </a></li>
         
        <?php if (empty($this->options->headerBlock) || in_array('ShowCategory', $this->options->headerBlock)): ?> 
        <?php $this->widget('Widget_Metas_Category_List')->to($categorys); ?>
        <?php while($categorys->next()): ?>
        <li class="page_item<?php if($this->is('category', $categorys->slug)): ?> current_page_item<?php endif; ?>"> <a href="<?php $categorys->permalink(); ?>" title="<?php $categorys->name(); ?>">
          <?php $categorys->name(); ?>
          </a></li>
        <?php endwhile; ?>
        <?php endif; ?>
        
        <?php if (empty($this->options->headerBlock) || in_array('ShowPage', $this->options->headerBlock)): ?> 
        <?php $this->widget('Widget_Contents_Page_List')->to($pages); ?>
        <?php while($pages->next()): ?>
        <li class="page_item<?php if($this->is('pages', $pages->slug)): ?> current_page_item<?php endif; ?>"><a href="<?php $pages->permalink(); ?>" title="<?php $pages->title(); ?>">
          <?php $pages->title(); ?>
          </a></li>
        <?php endwhile; ?>
        <?php endif; ?>
        
      </ul>
    </div>
  </div>
</div>
<!-- #header end --> 
