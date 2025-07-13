from flask import Blueprint, request, jsonify
from src.models.tech_support_knowledge import TechSupportKnowledge

knowledge_bp = Blueprint('knowledge', __name__)

# Initialize knowledge base
tech_knowledge = TechSupportKnowledge()

@knowledge_bp.route('/search', methods=['POST'])
def search_solutions():
    """
    Search for technical solutions based on query
    """
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        category = data.get('category')
        
        if not query:
            return jsonify({
                'error': 'Query is required',
                'status': 'error'
            }), 400
        
        # Find relevant solutions
        solutions = tech_knowledge.find_solution(query, category)
        
        # Format solutions for response
        formatted_solutions = []
        for solution in solutions:
            formatted_solutions.append({
                'id': solution.id,
                'title': solution.title,
                'description': solution.description,
                'category': solution.category,
                'difficulty': solution.difficulty,
                'estimated_time': solution.estimated_time,
                'steps': solution.steps,
                'troubleshooting_tips': solution.troubleshooting_tips,
                'keywords': solution.keywords
            })
        
        return jsonify({
            'solutions': formatted_solutions,
            'query': query,
            'category': category,
            'count': len(formatted_solutions),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@knowledge_bp.route('/solution/<solution_id>', methods=['GET'])
def get_solution(solution_id):
    """
    Get detailed information about a specific solution
    """
    try:
        solution = tech_knowledge.get_solution_by_id(solution_id)
        
        if not solution:
            return jsonify({
                'error': 'Solution not found',
                'status': 'error'
            }), 404
        
        # Get related solutions
        related_solutions = tech_knowledge.get_related_solutions(solution_id)
        
        return jsonify({
            'solution': {
                'id': solution.id,
                'title': solution.title,
                'description': solution.description,
                'category': solution.category,
                'difficulty': solution.difficulty,
                'estimated_time': solution.estimated_time,
                'prerequisites': solution.prerequisites,
                'steps': solution.steps,
                'troubleshooting_tips': solution.troubleshooting_tips,
                'related_issues': solution.related_issues,
                'keywords': solution.keywords
            },
            'related_solutions': [
                {
                    'id': rel.id,
                    'title': rel.title,
                    'category': rel.category,
                    'difficulty': rel.difficulty
                }
                for rel in related_solutions
            ],
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@knowledge_bp.route('/categories', methods=['GET'])
def get_categories():
    """
    Get all available solution categories
    """
    try:
        categories = {}
        
        for solution in tech_knowledge.solutions:
            category = solution.category
            if category not in categories:
                categories[category] = {
                    'name': category,
                    'count': 0,
                    'difficulties': set()
                }
            
            categories[category]['count'] += 1
            categories[category]['difficulties'].add(solution.difficulty)
        
        # Convert sets to lists for JSON serialization
        for category in categories.values():
            category['difficulties'] = list(category['difficulties'])
        
        return jsonify({
            'categories': list(categories.values()),
            'total_categories': len(categories),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@knowledge_bp.route('/quick-fix', methods=['POST'])
def get_quick_fix():
    """
    Get quick fix for common issues
    """
    try:
        data = request.get_json()
        issue_type = data.get('issue_type', '').strip()
        
        if not issue_type:
            return jsonify({
                'error': 'Issue type is required',
                'status': 'error'
            }), 400
        
        quick_fix = tech_knowledge.get_quick_fix(issue_type)
        
        if not quick_fix:
            return jsonify({
                'error': 'Quick fix not found for this issue type',
                'status': 'error'
            }), 404
        
        return jsonify({
            'quick_fix': quick_fix,
            'issue_type': issue_type,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@knowledge_bp.route('/diagnostic-questions/<category>', methods=['GET'])
def get_diagnostic_questions(category):
    """
    Get diagnostic questions for a specific category
    """
    try:
        questions = tech_knowledge.get_diagnostic_questions(category)
        
        if not questions:
            return jsonify({
                'error': 'No diagnostic questions found for this category',
                'status': 'error'
            }), 404
        
        return jsonify({
            'questions': questions,
            'category': category,
            'count': len(questions),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@knowledge_bp.route('/keywords', methods=['POST'])
def search_by_keywords():
    """
    Search solutions by multiple keywords
    """
    try:
        data = request.get_json()
        keywords = data.get('keywords', [])
        
        if not keywords or not isinstance(keywords, list):
            return jsonify({
                'error': 'Keywords array is required',
                'status': 'error'
            }), 400
        
        solutions = tech_knowledge.search_keywords(keywords)
        
        formatted_solutions = []
        for solution in solutions:
            formatted_solutions.append({
                'id': solution.id,
                'title': solution.title,
                'description': solution.description,
                'category': solution.category,
                'difficulty': solution.difficulty,
                'keywords': solution.keywords
            })
        
        return jsonify({
            'solutions': formatted_solutions,
            'keywords': keywords,
            'count': len(formatted_solutions),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@knowledge_bp.route('/category/<category>', methods=['GET'])
def get_solutions_by_category(category):
    """
    Get all solutions in a specific category
    """
    try:
        solutions = tech_knowledge.get_solutions_by_category(category)
        
        if not solutions:
            return jsonify({
                'error': 'No solutions found for this category',
                'status': 'error'
            }), 404
        
        formatted_solutions = []
        for solution in solutions:
            formatted_solutions.append({
                'id': solution.id,
                'title': solution.title,
                'description': solution.description,
                'difficulty': solution.difficulty,
                'estimated_time': solution.estimated_time,
                'keywords': solution.keywords
            })
        
        return jsonify({
            'solutions': formatted_solutions,
            'category': category,
            'count': len(formatted_solutions),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

