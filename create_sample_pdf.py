from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("data/test_sample.pdf", pagesize=letter)

content = """
TechCorp Product Catalog and Customer Support Guide

Welcome to TechCorp, your trusted partner in innovative software solutions. This comprehensive guide covers our product offerings, features, pricing, and customer support policies.

Page 1: Company Overview
TechCorp was founded in 2010 with a mission to empower businesses through cutting-edge technology. We specialize in productivity software, data analytics tools, and cloud services. Our products are designed to streamline operations, enhance decision-making, and drive growth for organizations of all sizes.

Our Core Values:
- Innovation: Constantly pushing boundaries with new technologies.
- Reliability: Ensuring 99.9% uptime for all services.
- Customer-Centric: Tailored solutions for unique business needs.
- Security: Enterprise-grade protection for sensitive data.

Page 2: Product Lineup
1. Productivity Suite Pro
   - Features: Document collaboration, task management, calendar integration.
   - Pricing: $29/user/month
   - Ideal for: Small to medium businesses

2. DataAnalytics Plus
   - Features: Real-time dashboards, predictive modeling, custom reports.
   - Pricing: $99/user/month
   - Ideal for: Data-driven organizations

3. CloudSync Enterprise
   - Features: Unlimited storage, automatic backups, multi-device sync.
   - Pricing: $19/user/month
   - Ideal for: Remote teams and distributed workforces

4. SecureComm Platform
   - Features: Encrypted messaging, video conferencing, file sharing.
   - Pricing: $39/user/month
   - Ideal for: Security-conscious enterprises

Page 3: Product Features in Detail
Productivity Suite Pro:
- Advanced document editing with real-time collaboration
- Integrated project management tools
- AI-powered scheduling assistant
- Mobile app for on-the-go access

DataAnalytics Plus:
- Drag-and-drop dashboard builder
- Machine learning algorithms for insights
- API integrations with popular databases
- Export capabilities in multiple formats

CloudSync Enterprise:
- End-to-end encryption
- Version control for all files
- Bandwidth optimization
- Compliance with GDPR and HIPAA

SecureComm Platform:
- Zero-knowledge encryption
- Screen sharing with annotations
- Recording capabilities
- Integration with existing workflows

Page 4: Pricing and Plans
All plans include:
- 24/7 customer support
- Free onboarding and training
- Regular feature updates
- Data migration assistance

Enterprise discounts available for 100+ users. Contact sales for custom quotes.

Page 5: Customer Support Policies
Our commitment to customer success:
- Response time: Within 2 hours for priority issues
- Support channels: Email, phone, live chat, knowledge base
- Service hours: 24/7 for critical issues, 9-5 business hours for general support
- Escalation process: Tier 1 to Tier 3 support specialists

Self-Service Resources:
- Comprehensive knowledge base
- Video tutorials and webinars
- Community forums
- API documentation

Page 6: Troubleshooting Common Issues
Issue: Unable to log in
Solution: Check internet connection, clear browser cache, reset password via forgot password link.

Issue: Slow performance
Solution: Close unnecessary applications, check system requirements, contact support for optimization tips.

Issue: Data sync errors
Solution: Verify account permissions, check firewall settings, run sync diagnostic tool.

Issue: Feature not working as expected
Solution: Review user manual, check for updates, submit detailed bug report.

Page 7: Frequently Asked Questions (FAQ)

Q: How do I upgrade my plan?
A: Log in to your account dashboard, go to Billing, and select Upgrade Plan. Changes take effect immediately.

Q: Can I cancel my subscription anytime?
A: Yes, you can cancel at any time. Refunds are prorated based on unused days.

Q: Is my data secure?
A: Absolutely. We use bank-level encryption and comply with industry standards like SOC 2 and ISO 27001.

Q: Do you offer training?
A: Yes, we provide free online training sessions and personalized onboarding for enterprise clients.

Q: What are your system requirements?
A: Minimum: Windows 10/MacOS 10.14, 4GB RAM, stable internet. Recommended: Windows 11/MacOS 11, 8GB RAM.

Q: How do I report a bug?
A: Use the in-app feedback tool or email support@techcorp.com with screenshots and steps to reproduce.

Q: Can I integrate with other tools?
A: Yes, our products support APIs and integrations with popular platforms like Slack, Microsoft Office, and Salesforce.

Q: What happens if I exceed my storage limit?
A: You'll receive a notification. Upgrade your plan or purchase additional storage to continue using the service.

Page 8: Contact Information
- General Support: support@techcorp.com
- Sales: sales@techcorp.com
- Billing: billing@techcorp.com
- Phone: 1-800-TECHCORP
- Address: 123 Tech Street, Silicon Valley, CA 94000

Page 9: Warranty and Guarantees
All products come with a 30-day money-back guarantee. Hardware components have a 1-year warranty. Software updates are provided free of charge during the subscription period.

Page 10: Future Roadmap
Upcoming features:
- AI-powered insights in DataAnalytics Plus
- Enhanced security features in SecureComm
- Mobile app improvements
- Integration with emerging technologies like blockchain

Thank you for choosing TechCorp. We're here to support your success.
"""

# Split content into lines and draw
lines = content.strip().split("\n")
y = 750
for line in lines:
    c.drawString(50, y, line)
    y -= 15
    if y < 50:
        c.showPage()
        y = 750

c.save()
