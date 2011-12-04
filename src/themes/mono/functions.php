<?php

if (!defined('__TYPECHO_ROOT_DIR__')) {
    exit;
}

function themeInit() {
}

function themeConfig($form) {
    $logoUrl = new Typecho_Widget_Helper_Form_Element_Text('logoUrl', NULL, NULL, _t('站点LOGO地址'), _t('用于替换网站标题的站点LOGO图片URL'));
    $form->addInput($logoUrl);
    
    $monoinfo = new Typecho_Widget_Helper_Form_Element_Text('monoinfo', NULL, NULL, 'Information', 'Display in sidebar.');
    $form->addInput($monoinfo);
    
    $postBlock = new Typecho_Widget_Helper_Form_Element_Checkbox('postBlock', array('relatedPost' => _t('显示相关文章')), array('relatedPost'), 'Display in post');
    $form->addInput($postBlock);
    
     $sidebarBlock = new Typecho_Widget_Helper_Form_Element_Checkbox('sidebarBlock', 
    array('ShowRecentPosts' => _t('显示最新文章'),
    'ShowRecentComments' => _t('显示最近回复'),
    'ShowAuthorComments' => _t('显示博主评论'),
    'ShowCategory' => _t('显示分类'),
    'ShowArchive' => _t('显示归档'),
    'ShowOther' => _t('显示其它杂项')),
    array('ShowRecentPosts', 'ShowRecentComments', 'ShowAuthorComments', 'ShowCategory', 'ShowArchive', 'ShowOther'), 'Display in sidebar');
    
    $form->addInput($sidebarBlock->multiMode());
    
     $headerBlock = new Typecho_Widget_Helper_Form_Element_Checkbox('headerBlock', 
    array('ShowCategory' => _t('显示分类'),
    'ShowPage' => _t('显示页面')),
    array('ShowCategory', 'ShowPage'), 'Display on top');
    
    $form->addInput($headerBlock->multiMode());
}