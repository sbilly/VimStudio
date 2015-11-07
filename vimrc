execute pathogen#infect() 




" 显示行号
set number
" 语法高亮
syntax on
" 智能缩进
set smartindent
" 字符编码自动识别
set fencs=utf-8,cp936
" 执行ctags生成标签文件
nnoremap <F5> :!ctags -R<CR>
filetype plugin on

" for taglist plugin 
" ------------------------------------------------------------------------
" 选择tag后自动关闭taglist窗口
"let Tlist_Close_On_Select = 1
" 紧凑样式的taglist
let Tlist_Compact_Format=1
" 如果只剩下taglist窗口则退出vim
let Tlist_Exit_OnlyWindow=1
" 在taglist窗口中显示原型
let Tlist_Display_Prototype=1
" 执行TlistToggle后将焦点移到taglist窗口
let Tlist_GainFocus_On_ToggleOpen=1
" 窗口位置在右
let Tlist_Use_Right_Window = 1
" 窗口宽度
let Tlist_WinWidth = 100
set updatetime=50
nnoremap <silent> <F8> :TlistToggle<CR>

" for nerdtree plugin 
" ------------------------------------------------------------------------
" 窗口位置在右
let g:NERDTreeWinPos="right"
" 窗口宽度
let g:NERDTreeWinSize=70
nnoremap <silent> <F9> :NERDTreeToggle<CR>

" for OmniCppComplete plugin 
" ------------------------------------------------------------------------
" configure tags - add additional tags here or comment out not-used ones
set tags+=~/.vim/tags/cpp
set tags+=~/.vim/tags/gl
set tags+=~/.vim/tags/sdl
set tags+=~/.vim/tags/qt4
" build tags of your own project with Ctrl-F12
map <C-F12> :!ctags -R --sort=yes --c++-kinds=+p --fields=+iaS --extra=+q .<CR>
" OmniCppComplete
let OmniCpp_NamespaceSearch = 1
let OmniCpp_GlobalScopeSearch = 1
let OmniCpp_ShowAccess = 1
let OmniCpp_ShowPrototypeInAbbr = 1 " show function parameters
let OmniCpp_MayCompleteDot = 1 " autocomplete after .
let OmniCpp_MayCompleteArrow = 1 " autocomplete after ->
let OmniCpp_MayCompleteScope = 1 " autocomplete after ::
let OmniCpp_DefaultNamespaces = ["std", "_GLIBCXX_STD"]
" automatically open and close the popup menu / preview window
au CursorMovedI,InsertLeave * if pumvisible() == 0|silent! pclose|endif
set completeopt=menuone,menu,longest,preview
