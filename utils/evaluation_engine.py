import pandas as pd
import numpy as np
from datetime import datetime
from collections import defaultdict
import json

class EvaluationEngine:
    def __init__(self):
        self.answer_keys = {}  # Store answer keys for different tests
    
    def set_answer_key(self, test_id, answer_key):
        """Set the answer key for a specific test"""
        self.answer_keys[test_id] = answer_key
    
    def calculate_score(self, candidate_answers, answer_key, negative_marking=False, negative_mark=0.25):
        """Calculate score based on candidate answers and answer key"""
        if len(candidate_answers) != len(answer_key):
            raise ValueError("Mismatch between candidate answers and answer key length")
        
        score = 0
        correct = 0
        incorrect = 0
        
        for i, (candidate_ans, correct_ans) in enumerate(zip(candidate_answers, answer_key)):
            if candidate_ans == correct_ans:
                score += 1
                correct += 1
            elif candidate_ans != '' and negative_marking:  # Only apply negative marking for attempted questions
                score -= negative_mark
                incorrect += 1
        
        # Ensure score doesn't go below 0
        score = max(0, score)
        
        return {
            'total_score': score,
            'percentage': (score / len(answer_key)) * 100,
            'correct': correct,
            'incorrect': incorrect,
            'unattempted': len(answer_key) - (correct + incorrect)
        }
    
    def calculate_improvement(self, pre_test_score, post_test_score):
        """Calculate improvement percentage between pre-test and post-test"""
        if pre_test_score == 0:
            if post_test_score > 0:
                return 100.0
            else:
                return 0.0
        return ((post_test_score - pre_test_score) / pre_test_score) * 100
    
    def identify_weak_areas(self, candidate_answers, answer_key, topics=None):
        """Identify weak areas based on incorrect answers"""
        if topics is None:
            # If no topics provided, just return question numbers
            incorrect_questions = []
            for i, (candidate_ans, correct_ans) in enumerate(zip(candidate_answers, answer_key)):
                if candidate_ans != correct_ans:
                    incorrect_questions.append(i+1)  # 1-indexed
            return {'weak_questions': incorrect_questions}
        
        # If topics provided, group by topics
        weak_topics = defaultdict(int)
        for i, (candidate_ans, correct_ans) in enumerate(zip(candidate_answers, answer_key)):
            if candidate_ans != correct_ans and i < len(topics):
                weak_topics[topics[i]] += 1
        
        # Sort by frequency of incorrect answers
        sorted_weak_topics = sorted(weak_topics.items(), key=lambda x: x[1], reverse=True)
        return {'weak_topics': dict(sorted_weak_topics)}
    
    def generate_batch_report(self, evaluations):
        """Generate batch-level analytics report"""
        if not evaluations:
            return {}
        
        scores = [eval_data['percentage'] for eval_data in evaluations.values()]
        
        return {
            'batch_average': np.mean(scores),
            'batch_median': np.median(scores),
            'batch_std_dev': np.std(scores),
            'highest_score': max(scores),
            'lowest_score': min(scores),
            'pass_count': sum(1 for score in scores if score >= 40),  # Assuming 40% pass mark
            'fail_count': sum(1 for score in scores if score < 40),
            'total_candidates': len(scores)
        }
    
    def generate_individual_report(self, candidate_id, pre_test_eval=None, post_test_eval=None):
        """Generate individual performance report"""
        report = {
            'candidate_id': candidate_id,
            'generated_at': datetime.now().isoformat()
        }
        
        if pre_test_eval:
            report['pre_test'] = pre_test_eval
        
        if post_test_eval:
            report['post_test'] = post_test_eval
        
        # Calculate improvement if both tests are available
        if pre_test_eval and post_test_eval:
            improvement = self.calculate_improvement(
                pre_test_eval['percentage'], 
                post_test_eval['percentage']
            )
            report['improvement_percentage'] = improvement
            
            # Determine performance trend
            if improvement > 20:
                trend = "Significant Improvement"
            elif improvement > 0:
                trend = "Moderate Improvement"
            elif improvement == 0:
                trend = "No Change"
            else:
                trend = "Decline"
            report['performance_trend'] = trend
        
        return report
    
    def recommend_training(self, weak_areas, department_skills):
        """Recommend training based on weak areas and department requirements"""
        recommendations = []
        
        # This is a simplified recommendation system
        # In practice, you'd have a more sophisticated matching algorithm
        
        for topic, count in weak_areas.get('weak_topics', {}).items():
            if topic in department_skills:
                priority = "High" if count > 3 else "Medium" if count > 1 else "Low"
                recommendations.append({
                    'topic': topic,
                    'priority': priority,
                    'recommended_hours': count * 2,  # Simplified calculation
                    'department_relevance': department_skills[topic]
                })
        
        return sorted(recommendations, key=lambda x: x['priority'])
    
    def evaluate_answers(self, candidate_answers, answer_key, pass_threshold=40):
        """Evaluate candidate answers against answer key and return results"""
        # Use existing calculate_score method to get evaluation results
        result = self.calculate_score(candidate_answers, answer_key)
        
        # Determine pass/fail status based on percentage (using configurable threshold)
        status = "pass" if result['percentage'] >= pass_threshold else "fail"
        result['status'] = status
        
        # Add candidate ID placeholder (will be set by caller)
        result['candidate_id'] = "unknown"
        
        return result

# Example usage
if __name__ == "__main__":
    engine = EvaluationEngine()
    
    # Example answer key
    answer_key = ['A', 'B', 'C', 'D', 'A', 'B', 'C', 'D', 'A', 'B']
    engine.set_answer_key('test_001', answer_key)
    
    # Example candidate answers
    candidate_answers = ['A', 'B', 'C', 'D', 'A', 'C', 'C', 'D', 'B', 'B']
    
    # Calculate score
    result = engine.calculate_score(candidate_answers, answer_key)
    print("Score Result:", result)
    
    # Calculate improvement
    improvement = engine.calculate_improvement(60, 85)
    print("Improvement:", improvement)
    
    print("Evaluation Engine loaded successfully!")