Motey
#####

|master_build| |development_build|

.. contents::

.. section-numbering::


What is Motey
=============

Motey is a fog node agent which is able to start virtual containers and can act autonomous.

Installation
============

Dependecies
-----------

Motey is using python 3.5 or newer. All the necessary requirements are in ``motey-docker-image/requirements.txt``.
A separate MQTT server is optional but recommended.

Docker
------

The easiest way to use Motey is to run the docker container.

.. code-block:: bash

    # pull the docker container.
    $ docker pull neoklosch/motey

    # run the container
    $ docker run -ti -v /var/run/docker.sock:/var/run/docker.sock -p 5023:5023 -p 5024:5024 -p 5090:5090 neoklosch/motey

    # to enter the container
    $ docker exec -ti <container_name> bash

Motey need a MQTT broker to communicate with other nodes. Therefore a MQTT server has to started.

.. code-block:: bash

    # pull the docker container.
    $ docker pull toke/mosquitto

    # run the container and load the config file from the scripts folder
    $ docker run -p 1883:1883 -p 9001:9001 -v ./scripts/config:/mqtt/config:ro toke/mosquitto

The ip of the server has to be configured in the ``config.ini`` file of Motey.

Install manually Linux
----------------------

.. code-block:: bash

    # clone Motey repo
    $ git clone https://github.com/Neoklosch/Motey.git

    # enter Motey folder
    $ cd Motey

    # build application
    $ python3 setup.py build

    # install application
    $ python3 setup.py install

Using Motey
===========

By default Motey is executed as a daemon.
It can be started, stopped and restarted via the cli tool.

.. code-block:: bash

    # start the service
    $ motey start

    # stop the service
    $ motey stop

    # restart the service
    $ motey restart

You also can start Motey in foreground.

.. code-block:: bash

    # start the application
    $ python3 /opt/motey/main.py


Motey Architecture
==================

.. class:: no-web

    .. image:: https://raw.githubusercontent.com/neoklosch/Motey/master/resources/images/motey_architecture.png
        :alt: Motey Architecture
        :width: 100%
        :align: center


.. |master_build| image:: https://travis-ci.org/Neoklosch/Motey.svg?branch=master&style=flat-square&label=master%20build
    :target: https://travis-ci.org/Neoklosch/Motey
    :alt: Build status of the master branch

.. |development_build| image:: https://travis-ci.org/Neoklosch/Motey.svg?branch=development&style=flat-square&label=master%20build
    :target: https://travis-ci.org/Neoklosch/Motey
    :alt: Build status of the development branch
