.. SPDX-License-Identifier: MIT OR Apache-2.0
   SPDX-FileCopyrightText: The Coding Guidelines Subcommittee Contributors

.. default-domain:: coding-guidelines

Exceptions and Errors
=====================

.. guideline:: Guideline titles
    :id: gui_DxRnsAt69H7b 
    :category: required
    :status: draft
    :release: 1.1.1-1.1.2
    :fls: fls_e5td0fa92fay
    :decidability: decidable
    :scope: system
    :tags: reduce-human-error

    Very amplified

    .. rationale:: 
        :id: rat_ThSEzAXvYJ3y 
        :status: draft

        Not reasonable

    .. non_compliant_example::
        :id: non_compl_ex_qjdo3TNflqvv 
        :status: draft

        Writing code is the entry point to software engineering, not the pinnacle.

        .. code-block:: rust

            macro_rules! vec {
                                  ( $( $x:expr ),* ) => {
                                      {
                                          let mut temp_vec = Vec::new(); // non-global path
                                          $(
                                              temp_vec.push($x);
                                          )*
                                          temp_vec
                                          }
                                      }
                                  };
                              }

    .. compliant_example::
        :id: compl_ex_YDMXJUNSBpbG 
        :status: draft

        Writing code is the entry point to software engineering, not the pinnacle.

        .. code-block:: rust

            macro_rules! vec {
                      ( $( $x:expr ),* ) => {
                          {
                              let mut temp_vec = ::std::vec::Vec::new(); // global path 
                              let mut temp_vec = ::std::vec::Vec::new(); // global path 
                              let mut temp_vec = ::std::vec::Vec::new(); // global path 
                              let mut temp_vec = ::std::vec::Vec::new(); // global path 
                              let mut temp_vec = ::std::vec::Vec::new(); // global path 

                              $(
                                  temp_vec.push($x);
                              )*
                              temp_vec
                              Update: ----
                          }
                      };
                  }
