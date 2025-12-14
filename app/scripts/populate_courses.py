from app import create_app
from app.config import db
from app.models import Course, Assignment, StudentAssignment

# adding courses to the db so we can test our functionality
def populate_courses():
    courses_data = [
         {
            'code': 'PHYS51',
            'title': 'General Physics II',
            'description': 'A calculus-based introduction to electricity and magnetism, covering electric charges, electric and magnetic fields, dc and ac circuits, and electromagnetic waves.',
            'credits': 4,
            'professor': 'John Doe',
            'availability': True,
            'format': 'online',
            'max_students': 30
        },
        {
            'code': 'CMPE131',
            'title': 'Software Engineering I',
            'description': 'Why software engineering? What is software engineering? Software development lifecycle activities: project planning and management requirements analysis, requirement specification. Software design, software testing, verification, validation, and documentation. Software quality assurance and review techniques, software maintenance, team-based projects.',
            'credits': 3,
            'professor': 'Carlos Rojas',
            'availability': True,
            'format': 'in-person',
            'max_students': 25
        },
        {
            'code': 'CMPE102',
            'title': 'Assembly Language Programming',
            'description': 'Assembly programming; assembly-C interface; CPU and memory organization; addressing modes; arithmetic, logic and branch instructions; arrays, pointers, subroutines, stack and procedure calls; software interrupts; multiplication, division and floating point arithmetic.',
            'credits': 3,
            'professor': 'Michael Brown',
            'availability': True,
            'format': 'in-person',
            'max_students': 20
        },
        {
            'code': 'ISE130',
            'title': 'Engineering Probability and Statistics',
            'description': 'Probability theory, graphical displays of data, graphical methods of comparisons of samples and hypotheses testing. Statistical estimation and inference. Uses graphical statistical packages.',
            'credits': 3,
            'professor': 'Emily Wilson',
            'availability': True,
            'format': 'in-person',
            'max_students': 28
        },
        {
            'code': 'ENGR10',
            'title': 'Introduction to Engineering',
            'description': 'Introduction to engineering through hands-on design projects, case studies, and problem-solving using computers. Students also acquire non-technical skills, such as team skills and the ability to deal with ethical dilemmas.',
            'credits': 3,
            'professor': 'David Lee',
            'availability': True,
            'format': 'online',
            'max_students': 40
        },
        {
            'code': 'CS49J',
            'title': 'Programming in Java',
            'description': 'Introduction to the Java programming language and libraries. Topics include fundamental data types and control structures, object-oriented programming, string processing, input/output, and error handling. Use of Java libraries for mathematics, graphics, collections, and for user interfaces.',
            'credits': 3,
            'professor': 'David Taylor',
            'availability': False, 
            'format': 'online',
            'max_students': 35
        }
    ]
    
    with create_app.app_context():
        # Check if courses already exist
        if Course.query.count() > 0:
            print("Courses already exist in database. Skipping population.")
            return
        
        # Create and add courses
        for course_data in courses_data:
            course = Course(**course_data)
            db.session.add(course)
        
        # Commit to database
        db.session.commit()
        
        print(f"{len(courses_data)} courses added to database")

if __name__ == '__main__':
    populate_courses()

