# Script to add category management routes to app.py

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Category routes to insert
category_routes = '''

# ==================== CATEGORY MANAGEMENT ROUTES ====================
@app.route('/admin/categories', methods=['GET', 'POST'])
@admin_required
def admin_categories():
    """Manage categories"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        icon = request.form.get('icon', 'fas fa-tag')
        color = request.form.get('color', '#4361ee')
        active = request.form.get('active') == 'on'

        cat_id = generate_category_id()
        cat_data = {
            'id': cat_id,
            'name': name,
            'description': description,
            'icon': icon,
            'color': color,
            'active': active,
            'destination_count': 0
        }
        save_category(cat_data)

        flash('Category added successfully!', 'success')
        return redirect(url_for('admin_categories'))

    all_categories = get_categories_data()
    all_destinations = get_destinations_data()

    # Calculate destination count for each category
    for cat_id, cat in all_categories.items():
        cat['destination_count'] = len([d for d in all_destinations.values() if d.get('category') == cat['name']])

    total_destinations = len(all_destinations)

    return render_template('admin/categories.html',
                         categories=all_categories,
                         total_destinations=total_destinations)


@app.route('/admin/category/edit/<cat_id>', methods=['POST'])
@admin_required
def admin_edit_category(cat_id):
    """Edit category"""
    category = get_category_data(cat_id)
    if not category:
        flash('Category not found!', 'error')
        return redirect(url_for('admin_categories'))

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        icon = request.form.get('icon', 'fas fa-tag')
        color = request.form.get('color', '#4361ee')
        active = request.form.get('active') == 'on'

        cat_data = {
            'name': name,
            'description': description,
            'icon': icon,
            'color': color,
            'active': active
        }
        update_category_data(cat_id, cat_data)

        flash('Category updated successfully!', 'success')
        return redirect(url_for('admin_categories'))

    return redirect(url_for('admin_categories'))


@app.route('/admin/category/delete/<cat_id>', methods=['POST'])
@admin_required
def admin_delete_category(cat_id):
    """Delete category"""
    category = get_category_data(cat_id)
    if not category:
        flash('Category not found!', 'error')
        return redirect(url_for('admin_categories'))

    # Check if any destinations use this category
    all_destinations = get_destinations_data()
    using_destinations = [d for d in all_destinations.values() if d.get('category') == category['name']]

    if using_destinations:
        flash(f'Cannot delete category! {len(using_destinations)} destination(s) are using it.', 'error')
        return redirect(url_for('admin_categories'))

    delete_category_data(cat_id)
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('admin_categories'))


@app.route('/api/categories')
def api_categories():
    """API endpoint for active categories"""
    all_categories = get_categories_data()
    active_categories = {k: v for k, v in all_categories.items() if v.get('active', True)}
    return jsonify(active_categories)

'''

# Find insertion point (before admin_init_firebase)
insert_point = content.find("@app.route('/admin/init-firebase')")
if insert_point != -1:
    content = content[:insert_point] + category_routes + '\n' + content[insert_point:]
    print('Category routes added successfully!')
else:
    print('Could not find insertion point!')

# Write back
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done!')
