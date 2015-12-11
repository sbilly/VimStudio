execute pathogen#infect() 

if $COLORTERM == 'gnome-terminal'
	set t_Co=256
endif

" don't beep
set visualbell
set noerrorbells
" 实时搜索
set incsearch
" vim命令行模式智能补全
set wildmenu
" 关闭兼容模式
set nocompatible
" 字体字号
"set guifont=Monaco:h20
" use YaHei.Consolas font.
set guifont=YaHei\ Consolas\ Hybrid\ 13 
" 显示行号
set number
" 禁止光标闪烁
set gcr=a:block-blinkon0
" 不显示滚动条
set guioptions-=l
set guioptions-=L
set guioptions-=r
set guioptions-=R
" 隐藏菜单和工具条
set guioptions-=m
set guioptions-=T
" 语法高亮
syntax enable
" 禁止折行
set nowrap
" 高亮显示搜索结果
set hlsearch
" 搜索时忽略大小写
set ignorecase
" 高亮当前行
set cursorline 
" 高亮显示当前列
set cursorcolumn
" 总是显示状态栏
set laststatus=2
" 智能缩进
set smartindent
" 字符编码自动识别
set fencs=utf-8,cp936
" 启动vim时不折叠代码
set nofoldenable
" 基于缩进进行代码折叠
set foldmethod=indent
" 基于语法进行代码折叠
set foldmethod=syntax
" 打开指定路径的文件
nnoremap <F8> :wincmd f<CR>
" 执行ctags生成标签文件
nnoremap <F2> :!ctags -R<CR><CR>
filetype plugin on

" 启用:Man命令查看各类man信息
source $VIMRUNTIME/ftplugin/man.vim
" 定义:Man命令查看各类man信息的快捷键(\man)
nmap <Leader>man :Man 2 <cword><CR>

" 一键编译
" ------------------------------------------------------------------------
" Save and make current file.o
function! Make()
	let curr_dir = expand('%:h')
	if curr_dir == ''
		let curr_dir = '.'
	endif
	echo curr_dir
	execute 'lcd ' . curr_dir
	execute 'make clean'
	execute 'make %:r.o'
	execute 'lcd -'
endfunction
nnoremap <F7> :update<CR>:call Make()<CR>
"nnoremap <silent> <F7> :make!<CR><CR>:cw<CR>

" 内容替换
" ------------------------------------------------------------------------
" 替换函数,参数说明：
" confirm：是否替换前逐一确认
" wholeword：是否整词匹配
" replace：被替换字符串
function! Replace(confirm, wholeword, replace)
	wa
	let flag = ''
	if a:confirm
		let flag .= 'gec'
	else
		let flag .= 'ge'
	endif
	let search = ''
	if a:wholeword
		let search .= '\<' . escape(expand('<cword>'), '/\.*$^~[') . '\>'
	else
		let search .= expand('<cword>')
	endif
	let replace = escape(a:replace, '/\&~')
	execute 'argdo %s/' . search . '/' . replace . '/' . flag . '| update'
endfunction
" 不确认、非整词
nnoremap <Leader>R :call Replace(0, 0, input('Replace '.expand('<cword>').' with: '))<CR>
" 不确认、整词
nnoremap <Leader>rw :call Replace(0, 1, input('Replace '.expand('<cword>').' with: '))<CR>
" 确认、非整词
nnoremap <Leader>rc :call Replace(1, 0, input('Replace '.expand('<cword>').' with: '))<CR>
" 确认、整词
nnoremap <Leader>rcw :call Replace(1, 1, input('Replace '.expand('<cword>').' with: '))<CR>
nnoremap <Leader>rwc :call Replace(1, 1, input('Replace '.expand('<cword>').' with: '))<CR>

" 调用wmctrl程序实现全屏 
" ------------------------------------------------------------------------
" 将外部命令wmctrl控制窗口最大化的命令行参数封装成一个vim 的函数
fun! ToggleFullscreen()
	call system("wmctrl -ir " . v:windowid . " -b toggle,fullscreen")
endf
" 全屏开/关快捷键
map <silent> <F11> :call ToggleFullscreen()<CR>
" 启动 vim 时自动全屏
autocmd VimEnter * call ToggleFullscreen()

" bduild-in: Quickfix
" ------------------------------------------------------------------------
" 窗口置于底部
autocmd FileType qf wincmd J

" pulgin: theme: vim-color-solarized
" ------------------------------------------------------------------------
syntax enable
set background=dark
colorscheme solarized

" pulgin: vim-headerguard 
" ------------------------------------------------------------------------
" 定制宏格式
function! g:HeaderguardName()
	return "__" . toupper(expand('%:t:gs/[^0-9a-zA-Z_]/_/g')) . "__"
endfunction 
nnoremap <F3> :HeaderguardAdd<CR>

" pulgin: gundo
" ------------------------------------------------------------------------
nnoremap <F1> :GundoToggle<CR>
let g:gundo_width=60
let g:gundo_preview_height=20


" plugin: YouCompleteMe
" ------------------------------------------------------------------------
" YCM 补全菜单配色
" 菜单
" highlight Pmenu ctermfg=2 ctermbg=3 guifg=#005f87 guibg=#EEE8D5
" 选中项
"highlight PmenuSel ctermfg=2 ctermbg=3 guifg=#AFD700 guibg=#106900
" 补全功能在注释中同样有效
let g:ycm_complete_in_comments=1
" 允许vim加载".ycm_extra_conf.py"文件,不再提示
let g:ycm_confirm_extra_conf=0
" 开启 YCM 标签补全引擎
let g:ycm_collect_identifiers_from_tags_files=1
" 引入C++标准库tags
set tags+=/data/misc/software/misc./vim/stdcpp.tags
" YCM集成OmniCppComplete补全引擎，设置其快捷键
" inoremap <leader>; <C-x><C-o>
" 补全内容不以分割子窗口形式出现，只显示补全列表
set completeopt-=preview
" 从第一个键入字符就开始罗列匹配项
let g:ycm_min_num_of_chars_for_completion=1
" 禁止缓存匹配项，每次都重新生成匹配项
let g:ycm_cache_omnifunc=0
" 语法关键字补全         
let g:ycm_seed_identifiers_with_syntax=1

" plugin: ctrlsf.vim
" ------------------------------------------------------------------------
" 全局搜索当前光标所在的关键字
nnoremap <Leader>sp :CtrlSF<CR>
" 不自动关闭结果窗口
let g:ctrlsf_auto_close = 0

" plugin: MiniBufExplorer
" ------------------------------------------------------------------------
" 自动启动，
let g:miniBufExplAutoStart=1
let g:miniBufExplMapWindowNavArrows=1 
let g:miniBufExplMapCTabSwitchBufs=1 
let g:miniBufExplModSelTarget=1 


" 显示/隐藏MiniBufExplorer窗口
"map <Leader>bl :MBEToggle<CR>
" buf切换
map <C-Tab> :MBEbn<CR>
map <C-S-Tab> :MBEbp<CR>


" plugin: vim-airline
" ------------------------------------------------------------------------
set laststatus=2

" plugin: vim-indent-guides
" ------------------------------------------------------------------------
" 打开vim时自动启动
let g:indent_guides_enable_on_vim_startup=0
" 从第二层开始可视化显示缩进
let g:indent_guides_start_level=2
" 色块宽度
let g:indent_guides_guide_size=0

" plugin: syntastic
" ------------------------------------------------------------------------
set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*
let g:syntastic_always_populate_loc_list = 1
let g:syntastic_auto_loc_list = 1
let g:syntastic_check_on_open = 1
let g:syntastic_check_on_wq = 0

" plugin: nerdtree 
" ------------------------------------------------------------------------
" 使用空格键
let NERDTreeMapActivateNode='<space>'
" 设置忽略的文件
let NERDTreeIgnore=['\.o', '\.swp', '\.pyc']
" 窗口位置在右
let g:NERDTreeWinPos="right"
" 窗口宽度
let g:NERDTreeWinSize=30
" 只剩下nerdtree窗口时关闭vim
autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTreeType") && b:NERDTreeType == "primary") | q | endif
" 启动vim时自动打开
autocmd vimenter * NERDTree
" 显示隐藏文件
let NERDTreeShowHidden=1
" 不显示帮助信息
let NERDTreeMinimalUI=1
" 删除文件时自动删除文件对应的buffer
let NERDTreeAutoDeleteBuffer=1

nnoremap <silent> <C-F10> :NERDTreeToggle<CR>
nnoremap <silent> <F10> :NERDTree<CR>


" plugin: tagbar
" ------------------------------------------------------------------------
" tagbar窗口中不显示多余的帮助信息 
let g:tagbar_compact=1
" 窗口宽度 
let tagbar_width=30 
" 窗口靠左显示
let tagbar_left=0
" 指定对哪些元素生成tag
let g:tagbar_type_cpp = {
	\ 'kinds' : [
		\ 'd:macros:1',
		\ 'g:enums',
		\ 't:typedefs:0:0',
		\ 'e:enumerators:0:0',
		\ 'n:namespaces',
		\ 'c:classes',
		\ 's:structs',
		\ 's:structs',
		\ 'u:unions',
		\ 'f:functions',
		\ 'm:members:0:0',
		\ 'v:global:0:0',
		\ 'x:external:0:0',
		\ 'l:local:0:0'
	\ ],
	\ 'sro'        : '::',
	\ 'kind2scope' : {
		\ 'g' : 'enum',
		\ 'n' : 'namespace',
		\ 'c' : 'class',
		\ 's' : 'struct',
		\ 'u' : 'union'
	\ },
	\ 'scope2kind' : {
		\ 'enum'      : 'g',
		\ 'namespace' : 'n',
		\ 'class'     : 'c',
		\ 'struct'    : 's',
		\ 'union'     : 'u'
	\ }
\ }

nnoremap <silent> <F11> :TagbarToggle<CR>

" plugin: taglist
" ------------------------------------------------------------------------
" 选择tag后自动关闭taglist窗口
"let Tlist_Close_On_Select = 1
" 紧凑样式的taglist
"let Tlist_Compact_Format=1
" 如果只剩下taglist窗口则退出vim
"let Tlist_Exit_OnlyWindow=1
" 在taglist窗口中显示原型
"let Tlist_Display_Prototype=1
" 执行TlistToggle后将焦点移到taglist窗口
"let Tlist_GainFocus_On_ToggleOpen=1
" 窗口位置(0:左,1:右)
"let Tlist_Use_Right_Window=1
" vim启动时自动打开
"let Tlist_Auto_Open=0
" 窗口宽度
"let Tlist_WinWidth=50
"set updatetime=50
" nnoremap <silent> <F8> :TlistToggle<CR>

" plugin: OmniCppComplete
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
autocmd CursorMovedI,InsertLeave * if pumvisible() == 0|silent! pclose|endif
set completeopt=menuone,menu,longest,preview
