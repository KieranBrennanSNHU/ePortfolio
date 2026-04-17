# Kieran Brennan ePortfolio
## CS499 Capstone

All narratives and program files reside in corresponding branches.

######Artifacts:
1. [CS 300: Binary Search Tree](https://github.com/KieranBrennanSNHU/ePortfolio/tree/CS-300-Data-Structures-and-Algorithms).
2. [IT 145: Hash Map](https://github.com/KieranBrennanSNHU/ePortfolio/tree/IT-145-Data-Structure-Revision).
3. [CS 340: SQLite](https://github.com/KieranBrennanSNHU/ePortfolio/tree/CS-340-Client-Server-Development).

### *Professional Self-Assessment*
  
  Throughout the Computer Science program at Southern New Hampshire University, I have honed for skills and tackled many different projects. Some of the attributes that best describe the work are: team-oriented, strong communication, concise technical skills, and an emphasis on security. In many courses, class discussion is a great way to interact with your peers professionally. Weekly discussions provided an incredible platform to take in critiques and positively influence my work. In CS 470: Full-Stack Development II, a fellow classmate's response to my discussion helped me better understand the pros of Amazon API Gateway. Although this type of communication and collaboration was short lived, it provides an insight into my willingness to work as a team and benefit from criticism. Often times communicating with coworkers is not enough. Communication with stakeholders is also essential in the software development world. In CS 250: Software Development Lifecycle, we focused on the individual roles that make up the Agile workflow. The Product Owner and Scrum Master typically communicate with stakeholders to ensure the product being developed meets the standards of the target goal. In CS 300: Data Structures and Algorithms, projects focused on data structures written in a multitude of languages. Structures that I am proficient in are Linked Lists, Hash Maps, and Binary Search Trees. Many projects throughout the CS program not only contain data structures but databases as well. The primary database used was MongoDB, but I have developed experience with other NoSQL databases like DynamoDB. The primary goal of the Computer Science degree at SNHU focuses on software engineering and security. CS 465: Full Stack Development encompasses this entirely. Throughout the course we developed a full MEAN stack to create a travel website application. To build our travel web application, we focused on the MVC (Model-View-Controller) architecture, which not only organized the project, but also improved security by separating concerns. 
  
  In this capstone, I have developed three different artifacts, each with its own benefits. The first artifact is a binary search tree data structure that is transposed from C++ into Python. Switching to a new language is meant to exhibit technical skills and strategies that can accomplish industry-specific goals. The next artifact also relates to data structures. This program reads data into separate arrays, and then the output prompts to add, delete, print, or quit the application. I demonstrate my knowledge of data structures by changing these arrays to HashMaps and providing the same functioning output. The final artifact is focused on databases. Throughout the Computer Science program, I learned about NoSQL and SQL databases. I have experience with MongoDB and DynamoDB but wanted to add more variety to my understanding. In the last part of the project, I focused on integrating SQLite into an application that previously used MongoDB. To accomplish this, I used DB Browser (SQLite), changed the application to read a csv file into the new SQLite database, and provided the same functionality as the previous code. All the artifacts highlighted above have been chosen to emphasis the focus on data structures, algorithms, and databases that I achieved at Southern New Hampshire University.

### *Code Review*

Click Here to visit my [code review](https://youtu.be/AMTUD9ArRdk).

### *Artifact One*
  
  <img width="2500" height="2000" alt="tree" src="https://github.com/user-attachments/assets/bbe40875-d543-404f-8714-6d58677f4024" />

  The artifact for this enhancement is a Binary Search Tree data structure that was created in CS 300: Data Structures and Algorithms. The program takes a csv file containing the names and class IDs of specific courses and fills out a binary search tree data structure with the corresponding data. The main function provides an options list to choose actions starting with reading in the data.csv courses file, reordering the search tree, searching for a specific course, and removing a specific course by course ID. The original program was written in C++, so for this enhancement the project was translated into python. I selected this item because it was a good way to familiarize myself with data structures in Python. By changing languages, I can articulate my knowledge of using multiple development languages. The artifact was improved by adding a reorder function and the flexibility of python. 
  
  The course outcomes met by this objective are as follows: Demonstrate an ability to use well-founded and innovative techniques, skills, and tools in computing practices for the purpose of implementing computer solutions that deliver value and accomplish industry-specific goals. Enhancing this project gave me more insight into pointers and how a binary search tree functions. I struggled with the syntax for creating a node that had self-pointers until I figured out the final method. This version creates the node as a class and defines its properties as self, class id, and class name. The self variable is used as a location for the node, whether that is right or left of the parent node. 

### *Artifact Two*

<img width="753" height="334" alt="Hashmap" src="https://github.com/user-attachments/assets/26ccb4b5-1ecb-4629-ba77-22a928ee4dfd" />

  For this project, I chose to revisit the IT 145 project that takes a list of monkeys and dogs and adds them to an array. I chose to change this data structure to a hashmap and integrate the new maps into the rest of the structure for the program. For example, I changed the output of the lists to use the HashMap when adding new animals or when printing out the existing ones. I left the old array intact to see the difference. 
  
  HashMaps are key value paired. This means that we can select a “key” for the user to search for when trying to access our map. In this case, I chose the animal's name as the key. Now the user can search for availability by name. Hashmaps offer constant time performance, or O(1). The user can input large amounts of data without increasing execution time. 
  
  The expertise in using different data structures is a valuable skill for any developer. I believe switching to a new data structure has exemplified my skill in the matter. I have full-filled the program outcome that states: Design and evaluate computing solutions that solve a given problem using algorithmic principles and computer science practices and standards appropriate to its solution, while managing the trade-offs involved in design choices (data structures and algorithms)
  
  While improving the existing project, I realized that HashMaps are a very strong way to store information that I do not typically use. I plan to use them more frequently especially with large amounts of input data, or times when a search key is used. 

### *Artifact Three*

<img width="260" height="127" alt="image" src="https://github.com/user-attachments/assets/1724ba08-b4de-4d5c-8565-e470f3ee2019" />

  This artifact is from the CS340, Client Server Development class. The purpose of the artifact is to read data from a csv file and output it to a Mongo database. The project has a main Jupyter Labs file and a python CRUD file. The purpose of the main Jupyter file is to interact between the database, read in the data, and make sure the user has the correct username and password. The CRUD file creates, reads, updates, and deletes from the database. 
  
  This artifact was included because it is a direct use case for interacting with databases. In this project that is specifically MongoDB, but in the enhancement, it is SQLite. This enhancement has shown my ability to integrate different types of database software. For this case, SQLite may not be a better database, but it is certainly good enough. 
  
  The course outcomes that I met with this project are as follows: Employ strategies for building collaborative environments that enable diverse audiences to support organizational decision making in the field of computer science. SQLite and MongoDB are different databases. SQLite is a relational database, which means it relies on tables and relationships between cells to create insights into the larger themes of the data. MongoDB is a NoSQL database that uses BSON or JSON like documents. It specializes in large amounts of data that may not all have the same componenets. In many situations, knowing which database to use is considered organizational decision making and is imperative to future strategies involved with the project. 
  
  While enhancing this artifact, I had a hard time integrating the username and password into the new file running SQLite. I found work around for it, but unfortunately the username and password are not used. Another issue I had was running Jupyter Notebooks to fill out my SQLite database. I ended up using a docker container to employ the necessary Jupyter plugins and imports. Using docker containers seems to be a great way to keep the environment simple.

<img width="1599" height="999" alt="SQLiteImage" src="https://github.com/user-attachments/assets/c693127a-cebf-45ff-a491-87fc32fef8aa" />


