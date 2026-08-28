import hashlib

class DocumentGenerator:
    """
    Service for converting various portfolio entities into standardized text documents.
    """
    
    @staticmethod
    def generate_project_document(project):
        content = f"Project Overview: {project.description or ''}\n\n"
        if hasattr(project, 'technologies') and project.technologies:
             content += f"Technologies: {project.technologies}\n\n"
             
        return {
            'title': project.title,
            'source_type': 'project',
            'source_id': str(project.id),
            'content': content.strip(),
            'metadata': {
                'slug': project.slug if hasattr(project, 'slug') else '',
            }
        }

    @staticmethod
    def generate_skill_document(skill):
        content = f"Skill: {skill.name}\n"
        if hasattr(skill, 'category') and skill.category:
             content += f"Category: {skill.category}\n"
            
        return {
            'title': skill.name,
            'source_type': 'skill',
            'source_id': str(skill.id),
            'content': content.strip(),
            'metadata': {
                'category': skill.category if hasattr(skill, 'category') else ''
            }
        }

    @staticmethod
    def generate_experience_document(exp):
        content = f"Role: {exp.role}\n"
        content += f"Company: {exp.company}\n"
        content += f"Duration: {exp.start_date} to {exp.end_date or 'Present'}\n"
        if exp.description:
            content += f"\nDescription:\n{exp.description}\n"
            
        return {
            'title': f"{exp.role} at {exp.company}",
            'source_type': 'experience',
            'source_id': str(exp.id),
            'content': content.strip(),
            'metadata': {
                'company': exp.company,
                'role': exp.role
            }
        }

    @staticmethod
    def generate_education_document(edu):
        content = f"Degree: {edu.degree}\n"
        content += f"Institution: {edu.institution}\n"
        content += f"Duration: {edu.start_date} to {edu.end_date or 'Present'}\n"
        if hasattr(edu, 'description') and edu.description:
             content += f"\nDescription:\n{edu.description}\n"
             
        return {
            'title': f"{edu.degree} at {edu.institution}",
            'source_type': 'education',
            'source_id': str(edu.id),
            'content': content.strip(),
            'metadata': {
                'institution': edu.institution
            }
        }

    @staticmethod
    def generate_profile_document(profile):
        content = f"Name: {profile.name}\n"
        if hasattr(profile, 'title') and profile.title:
            content += f"Title: {profile.title}\n"
        if hasattr(profile, 'bio') and profile.bio:
            content += f"\nBio:\n{profile.bio}\n"
        
        return {
            'title': profile.name,
            'source_type': 'profile',
            'source_id': str(profile.id),
            'content': content.strip(),
            'metadata': {}
        }
        
    @staticmethod
    def generate_certification_document(cert):
        content = f"Certification: {cert.name}\n"
        if hasattr(cert, 'issuer') and cert.issuer:
            content += f"Issuer: {cert.issuer}\n"
        if hasattr(cert, 'date_issued') and cert.date_issued:
            content += f"Date Issued: {cert.date_issued}\n"
            
        return {
            'title': cert.name,
            'source_type': 'certification',
            'source_id': str(cert.id),
            'content': content.strip(),
            'metadata': {}
        }

    @staticmethod
    def generate_github_document(repo):
        content = f"Repository: {repo.get('name')}\n"
        content += f"Description: {repo.get('description', 'No description')}\n"
        content += f"Language: {repo.get('language', 'Unknown')}\n"
        content += f"Topics: {', '.join(repo.get('topics', []))}\n"
        content += f"Stars: {repo.get('stargazers_count', 0)}\n"
        
        return {
            'title': repo.get('name'),
            'source_type': 'github',
            'source_id': str(repo.get('id')),
            'content': content.strip(),
            'metadata': {
                'url': repo.get('html_url')
            }
        }
