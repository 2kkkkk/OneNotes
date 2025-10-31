import os
import html
from datetime import datetime

def generate_blog_index(root_dir='.'):
    """
    生成三级目录结构的博客导航索引页面 - 简洁UI设计
    """
    
    # HTML页面模板 - 简洁UI设计
    html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>知识库索引</title>
    <style>
        :root {{
            --primary: #2563eb;
            --primary-light: #dbeafe;
            --secondary: #059669;
            --background: #ffffff;
            --surface: #f8fafc;
            --text-primary: #1f2937;
            --text-secondary: #6b7280;
            --border: #e5e7eb;
            --hover: #f3f4f6;
        }}

        [data-theme="dark"] {{
            --background: #111827;
            --surface: #1f2937;
            --text-primary: #f9fafb;
            --text-secondary: #d1d5db;
            --border: #374151;
            --hover: #374151;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: var(--text-primary);
            background: var(--background);
            min-height: 100vh;
            font-size: 16px;
            transition: all 0.2s ease;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        /* 简洁头部 */
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 40px 20px;
            border-bottom: 1px solid var(--border);
        }}
        
        .header h1 {{
            color: var(--text-primary);
            font-size: 2.2rem;
            margin-bottom: 10px;
            font-weight: 600;
        }}
        
        .header p {{
            color: var(--text-secondary);
            font-size: 1.1rem;
        }}
        
        /* 主题切换按钮 */
        .theme-toggle {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 8px 12px;
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 0.9rem;
            color: var(--text-secondary);
        }}
        
        .theme-toggle:hover {{
            background: var(--hover);
        }}
        
        /* 主要内容区域 */
        .main-content {{
            display: flex;
            flex-direction: column;
            gap: 30px;
            margin-bottom: 50px;
        }}
        
        /* 分类区域 */
        .category-section {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .category-header {{
            background: var(--primary-light);
            padding: 20px;
            border-bottom: 1px solid var(--border);
        }}
        
        .category-header h2 {{
            margin: 0;
            font-size: 1.4rem;
            font-weight: 600;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .category-count {{
            background: var(--primary);
            color: white;
            border-radius: 12px;
            padding: 4px 10px;
            font-size: 0.85rem;
            font-weight: 500;
        }}
        
        /* 子分类列表 */
        .subcategory-list {{
            list-style: none;
        }}
        
        .subcategory-item {{
            border-bottom: 1px solid var(--border);
            transition: background-color 0.2s ease;
        }}
        
        .subcategory-item:last-child {{
            border-bottom: none;
        }}
        
        .subcategory-item:hover {{
            background: var(--hover);
        }}
        
        .subcategory-header {{
            padding: 18px 20px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .subcategory-name {{
            font-weight: 500;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .subcategory-count {{
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}
        
        /* 笔记列表 */
        .notes-list {{
            list-style: none;
            padding: 0 20px 15px 40px;
            display: none;
        }}
        
        .notes-list.expanded {{
            display: block;
        }}
        
        .note-item {{
            margin: 8px 0;
            padding: 10px 12px;
            border-radius: 6px;
            transition: all 0.2s ease;
        }}
        
        .note-item:hover {{
            background: var(--hover);
        }}
        
        .note-link {{
            text-decoration: none;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.95rem;
        }}
        
        .note-link:hover {{
            color: var(--primary);
        }}
        
        /* 切换按钮 */
        .toggle-btn {{
            background: none;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 6px 12px;
            font-size: 0.85rem;
            cursor: pointer;
            margin-top: 10px;
            transition: all 0.2s ease;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        
        .toggle-btn:hover {{
            background: var(--hover);
            border-color: var(--primary);
        }}
        
        .hidden-notes {{
            display: none;
        }}
        
        /* 统计信息 */
        .stats {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 25px;
            margin-top: 30px;
        }}
        
        .stats h3 {{
            font-size: 1.2rem;
            margin-bottom: 20px;
            color: var(--text-primary);
            font-weight: 600;
            text-align: center;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }}
        
        .stat-item {{
            text-align: center;
            padding: 15px 10px;
            background: var(--background);
            border-radius: 6px;
            border: 1px solid var(--border);
        }}
        
        .stat-number {{
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--primary);
            display: block;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            color: var(--text-secondary);
            font-size: 0.85rem;
        }}
        
        .empty-message {{
            text-align: center;
            color: var(--text-secondary);
            padding: 40px 20px;
            font-style: italic;
        }}
        
        /* 响应式设计 */
        @media (max-width: 768px) {{
            .container {{
                padding: 15px;
            }}
            
            .header {{
                padding: 30px 15px;
                margin-bottom: 30px;
            }}
            
            .header h1 {{
                font-size: 1.8rem;
            }}
            
            .theme-toggle {{
                top: 15px;
                right: 15px;
                padding: 6px 10px;
            }}
            
            .notes-list {{
                padding: 0 15px 10px 30px;
            }}
            
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
    </style>
</head>
<body>
    <!-- 主题切换按钮 -->
    <div class="theme-toggle" id="themeToggle">
        <span>切换主题</span>
    </div>

    <div class="container">
        <div class="header">
            <h1>知识库索引</h1>
            <p>简洁的知识管理系统 · 共 {total_categories} 个知识领域</p>
        </div>
        
        <div class="main-content">
            {categories_content}
        </div>
        
        <div class="stats">
            <h3>知识统计</h3>
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
        // 主题切换功能
        const themeToggle = document.getElementById('themeToggle');
        const body = document.body;
        
        // 检查本地存储的主题偏好
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {{
            body.setAttribute('data-theme', 'dark');
            themeToggle.innerHTML = '<span>浅色模式</span>';
        }}
        
        themeToggle.addEventListener('click', () => {{
            if (body.getAttribute('data-theme') === 'dark') {{
                body.removeAttribute('data-theme');
                localStorage.setItem('theme', 'light');
                themeToggle.innerHTML = '<span>深色模式</span>';
            }} else {{
                body.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                themeToggle.innerHTML = '<span>浅色模式</span>';
            }}
        }});
        
        // 子分类展开/折叠功能
        document.addEventListener('DOMContentLoaded', function() {{
            // 为所有子分类标题添加点击事件
            document.querySelectorAll('.subcategory-header').forEach(header => {{
                header.addEventListener('click', function() {{
                    const notesList = this.nextElementSibling;
                    notesList.classList.toggle('expanded');
                    
                    // 更新箭头图标
                    const arrow = this.querySelector('.arrow');
                    if (arrow) {{
                        arrow.textContent = notesList.classList.contains('expanded') ? '▼' : '▶';
                    }}
                }});
            }});
            
            // 为所有切换按钮添加点击事件
            document.querySelectorAll('.toggle-btn').forEach(button => {{
                button.addEventListener('click', function(e) {{
                    e.stopPropagation(); // 防止触发父元素的点击事件
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
            
            // 重置缩放级别
            if (window.devicePixelRatio && window.devicePixelRatio !== 1) {{
                const meta = document.querySelector('meta[name="viewport"]');
                if (meta) {{
                    meta.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';
                }}
            }}
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
    
    def generate_categories_content(structure):
        """生成分类内容HTML，支持简洁UI和展开/折叠功能"""
        if not structure:
            return '<div class="empty-message">📝 暂无分类数据，请检查目录结构</div>'
        
        content_parts = []
        
        for main_category, sub_categories in sorted(structure.items()):
            if not sub_categories:
                continue
                
            # 计算该大类下的笔记总数
            category_note_count = sum(len(notes) for notes in sub_categories.values())
            
            category_html = '''
            <div class="category-section">
                <div class="category-header">
                    <h2>
                        {main_category}
                        <span class="category-count">{category_note_count} 篇</span>
                    </h2>
                </div>
                <ul class="subcategory-list">
            '''.format(
                main_category=html.escape(main_category),
                category_note_count=category_note_count
            )
            
            for sub_category, notes in sorted(sub_categories.items()):
                category_html += '''
                <li class="subcategory-item">
                    <div class="subcategory-header">
                        <div class="subcategory-name">
                            <span class="arrow">▶</span>
                            {sub_category}
                        </div>
                        <div class="subcategory-count">{note_count} 篇</div>
                    </div>
                    <ul class="notes-list">
                '''.format(
                    sub_category=html.escape(sub_category),
                    note_count=len(notes)
                )
                
                # 判断是否需要折叠
                if len(notes) > 5:
                    # 显示前5个笔记
                    for note in notes[:5]:
                        display_name = os.path.splitext(note['name'])[0]
                        category_html += '''
                        <li class="note-item">
                            <a class="note-link" href="{file_path}" target="_blank">
                                📄 {display_name}
                            </a>
                        </li>
                        '''.format(
                            file_path=html.escape(note['path']),
                            display_name=html.escape(display_name)
                        )
                    
                    # 隐藏剩余的笔记
                    category_html += '''
                    <div class="hidden-notes">
                    '''
                    
                    for note in notes[5:]:
                        display_name = os.path.splitext(note['name'])[0]
                        category_html += '''
                        <li class="note-item">
                            <a class="note-link" href="{file_path}" target="_blank">
                                📄 {display_name}
                            </a>
                        </li>
                        '''.format(
                            file_path=html.escape(note['path']),
                            display_name=html.escape(display_name)
                        )
                    
                    category_html += '''
                    </div>
                    <button class="toggle-btn">
                        ▼ 展开更多 ({hidden_count} 篇)
                    </button>
                    '''.format(hidden_count=len(notes) - 5)
                else:
                    # 显示全部笔记
                    for note in notes:
                        display_name = os.path.splitext(note['name'])[0]
                        category_html += '''
                        <li class="note-item">
                            <a class="note-link" href="{file_path}" target="_blank">
                                📄 {display_name}
                            </a>
                        </li>
                        '''.format(
                            file_path=html.escape(note['path']),
                            display_name=html.escape(display_name)
                        )
                
                category_html += '''
                    </ul>
                </li>
                '''
            
            category_html += '''
                </ul>
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
            if len(notes) > 5:
                folded_categories += 1
    
    print(f"其中 {folded_categories} 个小类的笔记数量超过5篇，已添加展开/折叠功能")
    
    # 生成内容
    categories_content = generate_categories_content(structure)
    
    # 生成完整的HTML
    generate_time = datetime.now().strftime("%Y-%m-%d")
    
    final_html = html_template.format(
        total_categories=total_categories,
        categories_content=categories_content,
        total_subcategories=total_subcategories,
        total_notes=total_notes,
        generate_time=generate_time
    )
    
    # 写入文件
    output_path = os.path.join(root_dir, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"简洁版导航页面已生成: {output_path}")
    print("🎯 页面特点:")
    print("  ✅ 简洁UI设计 - 无卡片，扁平化布局")
    print("  ✅ 默认字体大小 - 自然易读")
    print("  ✅ 深色/浅色主题切换")
    print("  ✅ 可折叠的子分类")
    print("  ✅ 响应式设计")
    print("  ✅ 展开/折叠功能（超过5个文件自动折叠）")
    print("  ✅ 缩放重置功能")

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