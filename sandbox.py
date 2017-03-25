from graphMachine import GraphMachine
from Utilities.constructors import *
from Utilities.pretty_representation import *
from Utilities.fileManager import FileManager

file_manager = FileManager()

# Test Data

# testData = " The wing was established in July 1950 and headquartered at Changi, on the east coast of Singapore. "
# testData = " Headquartered in the east coast, Singapore become Changi in July 1950"
# testData = " El burro de coolest Ross barfed happily nor sadly "
testData = " in the cup The 1998 FA Charity Shield was the 76th in a series of annual English football matches organised by The Football Association and usually played between the winners of the previous season's Premier League and FA Cup competitions. It was contested on 9 August 1998 by Arsenal, who won both titles the previous season, and Manchester United, the league runners-up. Watched by a crowd of 67,342 at Wembley Stadium (pictured), United began the game strongly, but Arsenal took the lead when Marc Overmars scored 11 minutes before half-time. They extended their lead in the second half, as Overmars and Nicolas Anelka found Christopher Wreh, who put the ball into an empty net at the second attempt. In the 72nd minute, Arsenal scored a third goal, when Anelka got around Jaap Stam in the penalty box and shot the ball past goalkeeper Peter Schmeichel. Arsenal won the match 30, United's first defeat in the Shield in 13 years. United completed a treble of trophies in the 199899 season, winning the league, the FA Cup and the UEFA Champions League. "
#testData = " aaron act "
testData = " Are you an innovative and collaborative developer who has a passion for creating rich user experiences? Are you seeking an opportunity to create software that helps make the world a better place? We are looking for a UX Developer to join our UX team in creating world-class software that helps companies to fulfill their sustainability missions more effectively. Position Summary You will partner with stakeholders to product owners, developers, to QA. You will help for creating solutions that delight users and allow them to spend more time focusing on their mission. This is a fantastic opportunity for you to express yourself through the company's vision and make a better world. Every day in Enablon Work closely with the product owner, testers and other software engineers. Collaborate within the UX team to determine approach and timelines. Able to understand highly complex products and turn those problems into easy-to-use solutions for customers. Understand the balance of creating a valuable UX with business needs and technical feasibility constraints to make tradeoffs where appropriate. Minimum Qualifications At least 3+ years of experience in designing web user interfaces using JS MVC frameworks (AngularJS, Backbone.js, ReactJS, etc) Unit Testing frameworks (Jasmine, Mocha, xUnit, NUnit) Modular JS development using: Browserify/RequireJS/Webpack Heavy experience in HTML, CSS and similar technologies .NET and C# are a plus but not required "
testData = " Job description Web Application Developer at Belvedere Trading Belvedere Trading is looking for a senior Web Application Developer with a proven experience for developing innovative, responsive web systems. Our Web Application Developer will participate in all aspects of the software development lifecycle, from design to testing to deployment. Successful candidates will have a proven track record of success, possess excellent problem solving abilities, and the ability to thrive in a collaborative, entrepreneurial environment. What our Web Application Developer does: The Web Application Developer will work in a team environment in the design and execution of web products with the potential to lead a team of other Web Application Developers. Belvedere Trading is looking for a self-starter with a track record of success and a drive to learn. The ideal candidate is a creative thinker who has had vast previous experience to user experience definition and user interface design. As a senior member of our team, successful candidates will direct their own learning, grow their expertise, and pass that knowledge on to other team members. At Belvedere, you work with the best, learn with the best, and create the best software we can imagine. More specifically, our Web Application Developer will: Lead web development projects and coach other developers Work closely with our product owners to ensure a positive and engaging user experience Create and maintain design standards Coordinate with project managers and team leadership to plan work Apply industry knowledge and technical skills in new and innovative ways Help to continuously improve team productivity, code quality, tool and technology adoption Create new features and help improve existing experiences Share ideas, experience, and knowledge with other members of the team Participate in code reviews Key qualities in great candidates: 2+ years of web development experience Business application development experience Experience writing clean, readable, and well-organized code Understanding of when to use the right tool for the job Experience with Relational Database Design, including SQL Experience with Service Oriented Architecture Experience with common web development technologies such as JavaScript, CSS, Django, Rails, ASP.Net, and JavaScript frameworks such as jQuery, Angular, Ember, or Knockout Experience with common web design patterns, protocols, and architectures such as MVC, SOAP, REST, WCF, and JSON Experience with web automation frameworks such as Selenium, Watir, Lettuce, or Cucumber A strong understanding of the nuances between different browsers and each of their limitations, and the ability to write efficient, cross-platform code Demonstrated ability to work in a fast-paced, mission-critical environment Careful attention to detail, and the vision and skill to push beyond expectations Demonstrated experience with all phases of the software development lifecycle Undergraduate degree in Computer Science, Computer Engineering, or a related field Great written and verbal communication skills  Job description Web Application Developer at Belvedere Trading Belvedere Trading is looking for a senior Web Application Developer with a proven experience for developing innovative, responsive web systems. Our Web Application Developer will participate in all aspects of the software development lifecycle, from design to testing to deployment. Successful candidates will have a proven track record of success, possess excellent problem solving abilities, and the ability to thrive in a collaborative, entrepreneurial environment. What our Web Application Developer does: The Web Application Developer will work in a team environment in the design and execution of web products with the potential to lead a team of other Web Application Developers. Belvedere Trading is looking for a self-starter with a track record of success and a drive to learn. The ideal candidate is a creative thinker who has had vast previous experience to user experience definition and user interface design. As a senior member of our team, successful candidates will direct their own learning, grow their expertise, and pass that knowledge on to other team members. At Belvedere, you work with the best, learn with the best, and create the best software we can imagine. More specifically, our Web Application Developer will: Lead web development projects and coach other developers Work closely with our product owners to ensure a positive and engaging user experience Create and maintain design standards Coordinate with project managers and team leadership to plan work Apply industry knowledge and technical skills in new and innovative ways Help to continuously improve team productivity, code quality, tool and technology adoption Create new features and help improve existing experiences Share ideas, experience, and knowledge with other members of the team Participate in code reviews Key qualities in great candidates: 2+ years of web development experience Business application development experience Experience writing clean, readable, and well-organized code Understanding of when to use the right tool for the job Experience with Relational Database Design, including SQL Experience with Service Oriented Architecture Experience with common web development technologies such as JavaScript, CSS, Django, Rails, ASP.Net, and JavaScript frameworks such as jQuery, Angular, Ember, or Knockout Experience with common web design patterns, protocols, and architectures such as MVC, SOAP, REST, WCF, and JSON Experience with web automation frameworks such as Selenium, Watir, Lettuce, or Cucumber A strong understanding of the nuances between different browsers and each of their limitations, and the ability to write efficient, cross-platform code Demonstrated ability to work in a fast-paced, mission-critical environment Careful attention to detail, and the vision and skill to push beyond expectations Demonstrated experience with all phases of the software development lifecycle Undergraduate degree in Computer Science, Computer Engineering, or a related field Great written and verbal communication skills  Job description Web Application Developer at Belvedere Trading Belvedere Trading is looking for a senior Web Application Developer with a proven experience for developing innovative, responsive web systems. Our Web Application Developer will participate in all aspects of the software development lifecycle, from design to testing to deployment. Successful candidates will have a proven track record of success, possess excellent problem solving abilities, and the ability to thrive in a collaborative, entrepreneurial environment. What our Web Application Developer does: The Web Application Developer will work in a team environment in the design and execution of web products with the potential to lead a team of other Web Application Developers. Belvedere Trading is looking for a self-starter with a track record of success and a drive to learn. The ideal candidate is a creative thinker who has had vast previous experience to user experience definition and user interface design. As a senior member of our team, successful candidates will direct their own learning, grow their expertise, and pass that knowledge on to other team members. At Belvedere, you work with the best, learn with the best, and create the best software we can imagine. More specifically, our Web Application Developer will: Lead web development projects and coach other developers Work closely with our product owners to ensure a positive and engaging user experience Create and maintain design standards Coordinate with project managers and team leadership to plan work Apply industry knowledge and technical skills in new and innovative ways Help to continuously improve team productivity, code quality, tool and technology adoption Create new features and help improve existing experiences Share ideas, experience, and knowledge with other members of the team Participate in code reviews Key qualities in great candidates: 2+ years of web development experience Business application development experience Experience writing clean, readable, and well-organized code Understanding of when to use the right tool for the job Experience with Relational Database Design, including SQL Experience with Service Oriented Architecture Experience with common web development technologies such as JavaScript, CSS, Django, Rails, ASP.Net, and JavaScript frameworks such as jQuery, Angular, Ember, or Knockout Experience with common web design patterns, protocols, and architectures such as MVC, SOAP, REST, WCF, and JSON Experience with web automation frameworks such as Selenium, Watir, Lettuce, or Cucumber A strong understanding of the nuances between different browsers and each of their limitations, and the ability to write efficient, cross-platform code Demonstrated ability to work in a fast-paced, mission-critical environment Careful attention to detail, and the vision and skill to push beyond expectations Demonstrated experience with all phases of the software development lifecycle Undergraduate degree in Computer Science, Computer Engineering, or a related field Great written and verbal communication skills "
#testData = """ "Job description. Note: By applying to this position your application is automatically submitted to the following locations: New York, NY, USA; Seattle, WA, USA; Washington, DC, USA; Austin, TX, USA; Mountain View, CA, USA; Chicago, IL, USA; Atlanta, GA, USA; Boulder, CO, USA. . Help businesses around the world "go Google." Google for Work teams work with schools, companies and government agencies to make them more productive, mobile and collaborative by using Google cloud computing to get their work done. As a Technical Curriculum Developer, you oversee all aspects of the Google for Work sales process, improving it with your insightful data analysis, troubleshooting, and seamless cross-functional teamwork. Your strategies ensure that companies new to Google products get the highest quality customer support and that the Google for Work program overall is kept on the cutting edge.. . Are you a code-savvy technical specialist looking to positively impact the people who use our cloud products? Well look no further! The Training and Certification Team is a rapidly growing organization within Google for Work seeking a passionate individual to develop a creative and engaging learning experience to help our customers succeed with the Google Cloud Platform products.. . As a Technical Curriculum Developer, you will work closely with technical subject matter experts (SMEs) to design, develop and maintain technical learning content and curricula for various cloud roles including Solution Architects, Developers, Data Scientists. To thrive in this job, you must be strong in instructional design, learning development principles and tools, cloud computing technologies and development languages, and have the ability to translate technical content into effective learning solutions.. . We've helped millions of employees and organizations around the world to "go Google." As masters of cloud computing, the Google for Work team helps small and large businesses, educational institutions and government agencies discover the wonders of "the cloud" and work smarter. Our technical and sales teams design and implement solutions for these organizations with custom features, security and support -- all with Google's philosophy of innovation and ease of use in mind.. . Responsibilities . Perform needs and task analysis, scope projects, and evaluate existing documentation to identify the most appropriate training approach and content to meet the learning needs of each audiences across multiple global locations.. Design and develop creative learner-centered training programs, modules, and materials in multiple modalities including synchronous remote learning methodologies, blended classroom learning, interactive e-learning modules, videos, device learning labs, job aides, facilitator guides and resource materials.. Develop valid training evaluation tools that evaluate behavioral and business impact.. Collaborate effectively with cross-functional SMEs and others to support initiatives.. Ensure and drive best practices standardization across all projects, content and sites.. Qualifications . . Minimum qualifications:. BA/BS degree in Computer Science, Instructional Design, Information Architecture, Technical Communications or related discipline or equivalent practical experience.. 5 years of experience in an instructional design role and 2 years of experience developing learning content for programmers, systems architects, systems administrators or related technical roles.. Experience with Camtasia, Adobe Captivate, Articulate Storyline, or similar e-learning development tools.. Preferred qualifications:. MBA or MA/MS degree in Computer Science, Instructional Design, Technical Communications or a related discipline.. CPLP or other learning/training certification.. Recent coding experience in one or more of the following languages, Java, .Net, Perl, PHP, Ruby or Python.. Experience creating and managing demonstration sites and labs.. Demonstrated knowledge of, and hands-on experience with cloud computing technologies.. Excellent communication, writing and editing skills for the purpose of knowledge transfer and skill development, including effectively explaining technical topics to novice or non-technical audiences. Ability to collaborate with highly technical subject matter experts and managers to develop training content and curricula.. To all recruitment agencies: Google does not accept agency resumes. Please do not forward resumes to our jobs alias, Google employees or any other company location. Google is not responsible for any fees related to unsolicited resumes.. At Google, we dont just accept difference - we celebrate it, we support it, and we thrive on it for the benefit of our employees, our products and our community. Google is proud to be an equal opportunity workplace and is an affirmative action employer. We are committed to equal employment opportunity regardless of race, color, ancestry, religion, sex, national origin, sexual orientation, age, citizenship, marital status, disability, gender identity or Veteran status. If you have a disability or special need that requires accommodation, please let us know." """
#testData = "Job description. As the worlds largest research organization, Nielsen is powered by talented creative scientists. Our Data Scientists come from diverse disciplines such as statistics, research methodology, mathematics, psychology, business, engineering and demography. These professionals drive innovation, new product ideation, experimental design and testing, complex analysis and delivery of data insights.. . The Data Scientists primary role will be to support the analytical needs for the Video/Scarborough team within the Product group. The role will include assisting with analysis, application of Nielsens proprietary methodologies, and developing, testing and facilitating implementation of statistical solutions to address specific issues or client needs.. . Job Responsibilities. Work as an integral member of the Video/Scarborough Sampling team in a time-critical production environment.. Assist in developing and automating methodologies in R and Python and identifying and recommending process improvements.. Maintain and update documented departmental procedures and metrics comprehensively and on a timely basis.. Query data from large relational databases for various analyses and/or requests, using SQL.. Monitor tools to better plan, predict and monitor sample performance at the survey and/or market level.. Work with cross-functional teams to design, implement and test new methodologies.. Confidently represent Data Science methods and approaches to internal and external partners and clients.. Work closely with internal customers and IT team to improve current processes and engineer new methods. This includes support with writing new software, testing and end-user requirements.. Detect, troubleshoot, and resolve data or system anomalies to support uninterrupted production and ensure data integrity.. Interaction with sample vendors to acquire sample.. Role Requirements. Undergraduate degree in mathematics, statistics, engineering, computer science, economics, business or fields that employ rigorous data analysis.. Strong verbal, presentation, and written skills. Critical thinking and creative problem solving skills. Accuracy and attention to detail. Experience creating, organizing and analyzing large datasets. Proficient in at least one statistical software package such as SAS, R or SPSS. Experience with scripting languages such as Python or SQL. Data visualization skills such as Spotfire or Tableau. Intellectual curiosity and persistence to find answers to questions. Knowledge of process improvement methodologies such as Lean or Six Sigma"
#testData = " The job requires experience with technologies such as python. "
#testData = " Experience with technologies. "

testData = " This is my job description. You need to develop with amazon robot engines. Not machine learning. "

# Set up ChainGraphLayer
originalChainGraphLayer = chainGraphLayerFromString(testData)
originalChainGraphLayer.classify([file_manager.load_data_type("letter.json")])
# print(originalChainGraphLayer)
#print(pretty_chainGraphLayer(originalChainGraphLayer))

# Create DataGraphMachine and feed data
flow_graphs = file_manager.load_flow_graphs(["word", "number", "punctuation"])
graphMachine = GraphMachine(originalChainGraphLayer)

graphMachine.chainGraphLayer = graphMachine.feed_chain_graph_layer(originalChainGraphLayer, flow_graphs)

#print(pretty_chainGraphLayer(graphMachine.chainGraphLayer))

graphMachine.chainGraphLayer.classify([file_manager.load_data_type("word.json"), file_manager.load_data_type("number.json")])

#print(pretty_chainGraphLayer(graphMachine.chainGraphLayer))

# Sentence Structures??
flow_graphs = file_manager.load_flow_graphs(["jobPostingSkill"])
graphMachine.chainGraphLayer = graphMachine.feed_chain_graph_layer(graphMachine.chainGraphLayer, flow_graphs)

#print(graphMachine.chainGraphLayer)
print(pretty_chainGraphLayer(graphMachine.chainGraphLayer))