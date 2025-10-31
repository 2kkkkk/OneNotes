import os
import html
from datetime import datetime

def generate_blog_index(root_dir='.'):
    """
    生成三级目录结构的博客导航索引页面，支持动态高度和展开/折叠功能
    
    Args:
        root_dir: 根目录路径，默认为当前目录
    """
    
    # HTML页面模板
    html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>我的知识库</title>
    <style>
        :root {{
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --accent-color: #e74c3c;
            --light-bg: #f8f9fa;
            --border-color: #e1e4e8;
            --shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 40px 20px;
            background: white;
            border-radius: 15px;
            box-shadow: var(--shadow);
            position: relative;
            overflow: hidden;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--secondary-color), var(--accent-color));
        }}
        
        .header h1 {{
            color: var(--primary-color);
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            color: #666;
            font-size: 1.1em;
        }}
        
        .category-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
            align-items: start; /* 确保卡片顶部对齐 */
        }}
        
        .main-category {{
            background: white;
            border-radius: 15px;
            box-shadow: var(--shadow);
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            /* 移除固定高度，让内容决定高度 */
            display: flex;
            flex-direction: column;
        }}
        
        .main-category:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }}
        
        .category-header {{
            background: linear-gradient(135deg, var(--primary-color), #34495e);
            color: white;
            padding: 20px;
            position: relative;
            /* 头部固定，不随内容变化 */
            flex-shrink: 0;
        }}
        
        .category-header h2 {{
            margin: 0;
            font-size: 1.4em;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .category-count {{
            background: var(--accent-color);
            color: white;
            border-radius: 20px;
            padding: 2px 10px;
            font-size: 0.8em;
            margin-left: auto;
        }}
        
        .category-content {{
            padding: 0;
            /* 内容区域自适应高度 */
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }}
        
        .sub-category {{
            padding: 15px 20px;
            border-bottom: 1px solid var(--border-color);
            transition: background-color 0.2s;
            /* 子分类也使用flex布局 */
            display: flex;
            flex-direction: column;
        }}
        
        .sub-category:last-child {{
            border-bottom: none;
        }}
        
        .sub-category:hover {{
            background: var(--light-bg);
        }}
        
        .sub-category-name {{
            font-weight: 600;
            color: var(--primary-color);
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .notes-list {{
            list-style: none;
            padding-left: 10px;
            /* 笔记列表自适应 */
            flex-grow: 1;
        }}
        
        .note-item {{
            margin: 8px 0;
            padding: 8px 12px;
            border-radius: 8px;
            transition: all 0.2s;
            border-left: 3px solid transparent;
        }}
        
        .note-item:hover {{
            background: var(--light-bg);
            border-left-color: var(--secondary-color);
            transform: translateX(5px);
        }}
        
        .note-link {{
            text-decoration: none;
            color: #555;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.95em;
        }}
        
        .note-link:hover {{
            color: var(--secondary-color);
        }}
        
        .toggle-btn {{
            background: var(--secondary-color);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 5px 12px;
            font-size: 0.8em;
            cursor: pointer;
            margin-top: 8px;
            transition: background-color 0.2s;
            display: flex;
            align-items: center;
            gap: 5px;
            align-self: flex-start; /* 按钮左对齐 */
        }}
        
        .toggle-btn:hover {{
            background: #2980b9;
        }}
        
        .hidden-notes {{
            display: none;
        }}
        
        .stats {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: var(--shadow);
            text-align: center;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 15px;
        }}
        
        .stat-item {{
            padding: 15px;
            background: var(--light-bg);
            border-radius: 10px;
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: var(--secondary-color);
            display: block;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.9em;
        }}
        
        .empty-message {{
            text-align: center;
            color: #999;
            padding: 40px;
            font-style: italic;
        }}
        
        /* 新增：根据内容量添加不同样式类 */
        .content-small {{
            /* 内容较少的大类卡片 - 不需要特殊处理，因为高度自适应 */
        }}
        
        .content-medium {{
            /* 内容中等的大类卡片 */
        }}
        
        .content-large {{
            /* 内容较多的大类卡片 */
            /* 可以添加最大高度和滚动，但这里我们选择完全自适应 */
        }}
        
        @media (max-width: 768px) {{
            .category-grid {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
            
            .container {{
                padding: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 我的知识库</h1>
            <p>系统化整理的知识笔记，共 {total_categories} 个知识领域</p>
        </div>
        
        <div class="category-grid">
            {categories_content}
        </div>
        
        <div class="stats">
            <h3>📊 知识库统计</h3>
            <div class="stats-grid">
                <div class="stat-item">
                    <span class="stat-number">{total_categories}</span>
                    <span class="stat-label">知识大类</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{total_subcategories}</span>
                    <span class="stat-label">子分类</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{total_notes}</span>
                    <span class="stat-label">笔记数量</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{generate_time}</span>
                    <span class="stat-label">更新日期</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        // 展开/折叠功能
        document.addEventListener('DOMContentLoaded', function() {{
            // 为所有切换按钮添加点击事件
            document.querySelectorAll('.toggle-btn').forEach(button => {{
                button.addEventListener('click', function() {{
                    const hiddenNotes = this.previousElementSibling;
                    const isHidden = hiddenNotes.classList.contains('hidden-notes');
                    
                    if (isHidden) {{
                        // 展开隐藏的笔记
                        hiddenNotes.classList.remove('hidden-notes');
                        this.innerHTML = '▲ 收起';
                    }} else {{
                        // 隐藏笔记
                        hiddenNotes.classList.add('hidden-notes');
                        this.innerHTML = '▼ 展开更多 (' + hiddenNotes.children.length + ' 篇)';
                    }}
                }});
            }});
        }});
    </script>
</body>
</html>'''
    
    def scan_directory_structure(root_dir):
        """扫描三级目录结构"""
        structure = {}
        total_notes = 0
        total_subcategories = 0
        
        # 遍历大类文件夹（一级目录）
        for main_category in os.listdir(root_dir):
            main_category_path = os.path.join(root_dir, main_category)
            
            # 跳过非文件夹和隐藏文件夹
            if not os.path.isdir(main_category_path) or main_category.startswith('.'):
                continue
            
            structure[main_category] = {}
            
            # 遍历小类文件夹（二级目录）
            for sub_category in os.listdir(main_category_path):
                sub_category_path = os.path.join(main_category_path, sub_category)
                
                if not os.path.isdir(sub_category_path) or sub_category.startswith('.'):
                    continue
                
                # 查找htm文件（三级目录）
                htm_files = []
                for file in os.listdir(sub_category_path):
                    if file.lower().endswith(('.htm', '.html')):
                        # 构建相对路径
                        file_path = os.path.join(main_category, sub_category, file)
                        htm_files.append({
                            'name': file,
                            'path': file_path.replace('\\', '/')
                        })
                
                if htm_files:
                    # 按文件名排序
                    htm_files.sort(key=lambda x: x['name'].lower())
                    structure[main_category][sub_category] = htm_files
                    total_notes += len(htm_files)
                    total_subcategories += 1
        
        return structure, total_notes, total_subcategories
    
    def get_content_size_class(note_count):
        """根据笔记数量返回内容大小分类"""
        if note_count <= 10:
            return "content-small"
        elif note_count <= 30:
            return "content-medium"
        else:
            return "content-large"
    
    def generate_categories_content(structure):
        """生成分类内容HTML，支持动态高度和展开/折叠功能"""
        if not structure:
            return '<div class="empty-message">📝 暂无分类数据，请检查目录结构</div>'
        
        content_parts = []
        
        for main_category, sub_categories in sorted(structure.items()):
            if not sub_categories:
                continue
                
            # 计算该大类下的笔记总数
            category_note_count = sum(len(notes) for notes in sub_categories.values())
            
            # 根据内容量确定CSS类
            content_class = get_content_size_class(category_note_count)
            
            category_html = f'''
            <div class="main-category {content_class}">
                <div class="category-header">
                    <h2>
                        📂 {html.escape(main_category)}
                        <span class="category-count">{category_note_count} 篇</span>
                    </h2>
                </div>
                <div class="category-content">
            '''
            
            for sub_category, notes in sorted(sub_categories.items()):
                category_html += f'''
                <div class="sub-category">
                    <div class="sub-category-name">
                        📁 {html.escape(sub_category)}
                        <span style="margin-left: auto; font-size: 0.8em; color: #666;">
                            {len(notes)} 篇
                        </span>
                    </div>
                    <ul class="notes-list">
                '''
                
                # 判断是否需要折叠
                if len(notes) > 3:
                    # 显示前5个笔记
                    for note in notes[:3]:
                        display_name = os.path.splitext(note['name'])[0]
                        category_html += f'''
                        <li class="note-item">
                            <a class="note-link" href="{html.escape(note['path'])}" target="_blank">
                                📄 {html.escape(display_name)}
                            </a>
                        </li>
                        '''
                    
                    # 隐藏剩余的笔记
                    category_html += f'''
                    <div class="hidden-notes">
                    '''
                    
                    for note in notes[3:]:
                        display_name = os.path.splitext(note['name'])[0]
                        category_html += f'''
                        <li class="note-item">
                            <a class="note-link" href="{html.escape(note['path'])}" target="_blank">
                                📄 {html.escape(display_name)}
                            </a>
                        </li>
                        '''
                    
                    category_html += f'''
                    </div>
                    <button class="toggle-btn">
                        ▼ 展开更多 ({len(notes) - 3} 篇)
                    </button>
                    '''
                else:
                    # 显示全部笔记
                    for note in notes:
                        display_name = os.path.splitext(note['name'])[0]
                        category_html += f'''
                        <li class="note-item">
                            <a class="note-link" href="{html.escape(note['path'])}" target="_blank">
                                📄 {html.escape(display_name)}
                            </a>
                        </li>
                        '''
                
                category_html += '''
                    </ul>
                </div>
                '''
            
            category_html += '''
                </div>
            </div>
            '''
            content_parts.append(category_html)
        
        return '\n'.join(content_parts)
    
    # 执行扫描
    print("正在扫描三级目录结构...")
    structure, total_notes, total_subcategories = scan_directory_structure(root_dir)
    total_categories = len(structure)
    
    print(f"找到 {total_categories} 个大类，{total_subcategories} 个小类，{total_notes} 个笔记文件")
    
    # 统计需要折叠的小类数量
    folded_categories = 0
    for main_category, sub_categories in structure.items():
        for sub_category, notes in sub_categories.items():
            if len(notes) > 3:
                folded_categories += 1
    
    print(f"其中 {folded_categories} 个小类的笔记数量超过5篇，已添加展开/折叠功能")
    
    # 生成内容
    categories_content = generate_categories_content(structure)
    
    # 生成完整的HTML
    generate_time = datetime.now().strftime("%Y-%m-%d")
    
    final_html = html_template.format(
        categories_content=categories_content,
        total_categories=total_categories,
        total_subcategories=total_subcategories,
        total_notes=total_notes,
        generate_time=generate_time
    )
    
    # 写入文件
    output_path = os.path.join(root_dir, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"导航页面已生成: {output_path}")
    print("页面特点:")
    print("  ✅ 三级目录清晰展示")
    print("  ✅ 动态高度调整 - 卡片高度根据内容自适应")
    print("  ✅ 展开/折叠功能（超过5个文件自动折叠）")
    print("  ✅ 响应式网格布局")
    print("  ✅ 悬停动画效果")
    print("  ✅ 统计信息面板")
    print("  ✅ 现代化美观设计")

def scan_and_preview(root_dir='.'):
    """
    快速扫描并预览目录结构
    """
    print("目录结构预览:")
    print("=" * 50)
    
    # 统计每个大类的笔记数量
    category_stats = {}
    
    for main_category in os.listdir(root_dir):
        main_path = os.path.join(root_dir, main_category)
        if os.path.isdir(main_path) and not main_category.startswith('.'):
            note_count = 0
            sub_count = 0
            
            for sub_category in os.listdir(main_path):
                sub_path = os.path.join(main_path, sub_category)
                if os.path.isdir(sub_path) and not sub_category.startswith('.'):
                    # 统计htm文件
                    htm_files = [f for f in os.listdir(sub_path) 
                                if f.lower().endswith(('.htm', '.html'))]
                    htm_count = len(htm_files)
                    note_count += htm_count
                    sub_count += 1
                    
            category_stats[main_category] = {'notes': note_count, 'subs': sub_count}
    
    # 按笔记数量排序并显示
    for category, stats in sorted(category_stats.items(), key=lambda x: x[1]['notes'], reverse=True):
        size_label = "内容较少" if stats['notes'] <= 10 else "内容中等" if stats['notes'] <= 30 else "内容较多"
        print(f"📂 {category}: {stats['notes']} 篇笔记, {stats['subs']} 个子类 ({size_label})")
    
    print("=" * 50)

if __name__ == "__main__":
    # 先预览目录结构
    scan_and_preview()
    
    # 生成导航页面
    generate_blog_index()
    
    # 如果需要指定其他目录，可以这样使用：
    # generate_blog_index('/path/to/your/notes/folder')