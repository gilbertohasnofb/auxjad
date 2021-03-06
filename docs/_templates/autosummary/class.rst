{{ objname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :members:
   :inherited-members:
   :special-members: __init__, __repr__, __len__, __call__, __next__, __iter__, __getitem__, __setitem__, __delitem__

   {% block methods %}

   {% if methods %}
   .. rubric:: {{ ('Methods') }}

   .. autosummary::
   {% for item in all_methods %}
      {%- if not item.startswith('_') or item in ['__init__',
                                                  '__repr__',
                                                  '__len__',
                                                  '__call__',
                                                  '__next__',
                                                  '__iter__',
                                                  '__getitem__',
                                                  '__setitem__',
                                                  '__delitem__',
                                                  ] %}
      ~{{ name }}.{{ item }}
      {%- endif -%}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block attributes %}
   {% if attributes %}
   .. rubric:: {{ ('Attributes') }}

   .. autosummary::
   {% for item in attributes %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

.. include:: ../api/abjad-targets.rst
.. include:: ../api/auxjad-targets.rst
