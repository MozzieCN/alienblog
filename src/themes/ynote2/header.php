<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head profile="http://gmpg.org/xfn/11">
<meta http-equiv="content-type" content="text/html; charset=<?php $this->options->charset(); ?>" />
<title><?php $this->archiveTitle(' &gt; ', '', ' - '); ?><?php $this->options->title(); ?></title>

<link rel="stylesheet" type="text/css" media="all" href="<?php $this->options->themeUrl('style.css?20110903'); ?>" />
<script type="text/javascript" src="http://jqueryjs.googlecode.com/files/jquery-1.3.2.min.js"></script>
<script language='javascript' src='<?php $this->options->themeUrl('base.js'); ?>'></script>
<script type="text/javascript">if (top.location != self.location){top.location=self.location;}</script> 

<?php $this->header("generator=&template="); ?>
</head>
<body> 
<div id="wrap"> 
    <div id="header"> 
        <div id="blog_title"> 
            <h1><a href="<?php $this->options->siteUrl(); ?>"><?php $this->options->title() ?></a></h1> 
            <div id="blog-description"><?php $this->options->description() ?></div> 
        </div>   
    </div>
