from django.db import models

from django .contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

User=get_user_model()
class Resume(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='resumes')
    file=models.FileField(upload_to='resumes/',validators=[FileExtensionValidator(allowed_extensions=['pdf','docx'])])
    orginal_text=models.TextField(blank=True)
    parsed_data=models.JSONField(default=dict)
    processing_status=models.CharField(
        max_length=20,
        choices=[
            ('uploaded','Uploaded'),
            ('processing','Processing'),
            ('processed','Processed'),
            ('failed','Failed'),
        ],
        default='uploaded'
    )
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    class Meta:
        ordering=['-created_at']

    def __str__(self):
        return f"Resume {self.id} - {self.user.email}"
    
class JobPosting(models.Model):
        JOB_TYPES=[
            ('full-time','Full-time'),
            ('part-time','Part-time'),
            ('internship','Internship'),
            ('contract','Contract'),
            ('remote','Remote')
        ]
        title=models.CharField(max_length=255)
        company=models.CharField(max_length=255)
        description=models.TextField()
        preferred_skills=models.JSONField(default=list)
        experience_required=models.PositiveIntegerField(default=0)
        job_type=models.CharField(max_length=20,choices=JOB_TYPES)
        location=models.CharField(max_length=255)
        posted_at=models.DateField(auto_now_add=True)
        is_active=models.BooleabField(default=True)

        class Meta:
            ordering=['-posted_at']
            indexes=[models.Index(fields=['title']),
                     models.Index(fields=['company']),
                     models.Index(fields=['job_type']),
                     ]
            
        def __str__(self):
            return f"{self.title} - {self.company}" 


class ResumeJobMatch(models.Model):
     resume=models.ForeignKey(Resume,on_delete=models.CASCADE,related_name='matches')
     job=models.ForeignKey(JobPosting, on_delete=models.CASCADE,related_name='matches')
     match_score=models.FloatField()
     skills_match=models.JSONField(default=list)
     missing_skills=models.JSONField(default=list)
     created_at=models.DateTimeField(auto_now_add=True)

     class Meta:
          unique_together=('resume','job')
          ordering=['-match_score']
     def __str__(self):
          return f"match {self.match_score}% - Resume {self.resume.id} to job {self.job.id}" 

     