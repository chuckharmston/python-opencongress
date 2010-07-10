A Python interface to the OpenCongress.org API.

Installation
============

python-opencongress is a simple Python module that is installable by placing the ``opencongress`` directory onto your system path.

As it is available on the Python Package Index, you can install python-opencongress using your favorite package manager::

   pip install python-opencongress
   
   easy_install python-opencongress

You can also install directly from the git master branch using the pip package manager::

   pip install git+http://github.com/cpharmston/python-opencongress.git#egg=opencongress

Or you can download python-opencongress and install locally::

   setup.py install

Usage
=====

The OpenCongress.org API is exposed via the ``opencongress.Api`` class. To create an instance of the class::
   
   import opencongress
   api = opencongress.Api('your_api_key_here')

Substituing ``your_api_key_here`` for your own API key, which can be obtained at the `API documentation page <http://www.opencongress.org/api>`_.

Most OpenCongress.org API functionality is available through the ``opencongress.Api`` class. For example, to view a list of all bills introduced during the `111th Congress <http://en.wikipedia.org/wiki/111th_United_States_Congress>`_::

   >>> api.bills(congress=111)
   [
      <OpenCongress Bill object (H.R.5472 America RISING Act of 2010)>,
      <OpenCongress Bill object (H.R.2521 National Infrastructure Development Bank Act of 2009)>,
      <OpenCongress Bill object (H.R.5473 Investing Income at Home Act of 2010)>,
      <OpenCongress Bill object (H.R.5455 New Philadelphia, Illinois, Study Act)>,
      <OpenCongress Bill object (H.R.5454 Reduce Unnecessary Spending Act of 2010)>,
      ...
   ]

To view a list of all congresspeople who are members (by name) of the `Kennedy family <http://en.wikipedia.org/wiki/Kennedy_family>`_ and Democrat party::

   >>> api.people(last_name='Kennedy')
   [
      <OpenCongress Person object (Ambrose Kennedy)>,
      <OpenCongress Person object (Andrew Kennedy)>,
      <OpenCongress Person object (Sen. Edward Kennedy [D, MA])>,
      <OpenCongress Person object (Joseph Kennedy)>,
      <OpenCongress Person object (Martin Kennedy)>,
      <OpenCongress Person object (Michael Kennedy)>,
      <OpenCongress Person object (Rep. Patrick Kennedy [D, RI-1])>,
      <OpenCongress Person object (Robert Kennedy)>,
      <OpenCongress Person object (William Kennedy)>
   ]

For a full list of API methods, see the ``pydoc``-generated inspection of the Api object at ``api_reference.txt``, included with this package and available at `python-opencongress' GitHub page <http://github.com/cpharmston/python-opencongress>`_.