# Web-App-Classification-of-Compact-Surfaces
#### Video Demo:  <https://youtu.be/viZ3hHXuxVY>
#### Description:

In a previous project, I developed an algorithm to classify compact surfaces, which you can explore here: [GitHub - Compact Surfaces](https://github.com/gonzalocancio/Compact-Surfaces). While that project focused heavily on the algorithm itself, it wasn’t particularly user-friendly, requiring users to interact directly with the code through the terminal. For this reason, I decided to create a new project that builds on the algorithm but aims to provide a much more accessible and interactive user experience.

This new project is a web application that simplifies the process of interacting with the classification algorithm. Built using Flask, the application allows users to input the necessary data in a much easier and more structured manner than before. Instead of working directly with the code, users can now input their data through a clean web interface that guides them through the process of specifying the polygon representing the compact surface they want to classify. This includes providing the polygon's vertices, the orientations of the edges, and the correct pairing of edges that should be glued together.

How the Application Works:
At the heart of the application is the idea that compact surfaces can be represented by a polygon, with its edges attached in pairs in a particular direction. The user must provide the polygon, indicate the correct orientation of the edges, and pair the edges that are to be "glued" together. Once this information is provided, the algorithm performs its classification, which involves determining whether the surface is orientable or non-orientable and computing its genus.

One of the core features of this project is the clear and organized flow between different stages of the process. The web application comprises two main pages, each serving a specific role in the interaction. The web is structured by three HTML files: layout.html, input.html, and output.html.

The layout.html file provides the general structure and appearance of the web interface. It defines the common elements that are shared across all pages, such as the header, navigation, and footer.
The input.html file is where the user begins. Upon accessing the web application, the user is immediately directed to this page, which prompts them to provide the required information about the compact surface. The interface here is dynamic and interactive, utilizing JavaScript to allow the user to create a polygon with labeled vertices, select the orientation of the edges, and specify how the edges should be paired. This interaction with the web allows the user to provide as input the exact representation of the surface the user is trying to classify.
After the user submits the surface data, they are redirected to the output.html page. This page contains the result of the classification algorithm and provides the relevant algebraic groups that correspond to the surface. The logic for determining and displaying the results is integrated into the file, ensuring that the user receives immediate feedback on the properties of the surface they have created.
Technical Details:
The transition between these pages is managed by the app.py file. This Python script leverages Flask to handle requests and responses. For example, when the user provides the input, the data is processed by the Flask application, which runs the classification algorithm in the backend. Once the classification is complete, Flask serves the result by rendering the output.html page.

The logic behind the classification is relatively straightforward but requires some mathematical background. Essentially, compact surfaces can be classified based on two criteria: whether they are orientable or non-orientable, and their genus. The genus of a surface refers to the number of "holes" it contains. The classification is provided together with the information of some of the algebraic groups associated to the surface: the homology groups and the fundamental group of the surface. These algebraic groups can be determined using simple formulas that depend on the genus of the surface and its orientability. Once the surface is classified, the web application presents the homology and fundamental groups as part of the output.

Further Enhancements:
In this project, I wanted to ensure the application not only helps users classify compact surfaces but also deepens their understanding of the underlying mathematics. Therefore, I added some additional features to make the web application more informative. After the surface is classified, the algebraic groups are displayed using LaTeX formatting to ensure they are presented clearly in a style and notation familiar to any mathematician.

One of the key attributes of the web application is that it simplifies what would otherwise be a complex task. While the classification of compact surfaces can be done manually, the process is tedious and prone to error. By automating the process and providing a clear visual interface, this web application makes it easier for both mathematicians and students to experiment with different surfaces and explore their properties.

In the future, I plan to expand the functionality of this web application by allowing the user to just draw the polygon and then recognise the image with a neural network that provides the right input to the classification algorithm.

For now, the focus is on making the web application a user-friendly tool for classifying compact surfaces and exploring their fundamental and homology groups.
