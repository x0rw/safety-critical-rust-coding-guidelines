.. SPDX-License-Identifier: MIT OR Apache-2.0
   SPDX-FileCopyrightText: The Coding Guidelines Subcommittee Contributors

.. default-domain:: coding-guidelines

Associated Items
================

.. guideline:: Guideline Test
    :id: gui_RZxGmF2THr4k 
    :category: advisory
    :status: draft
    :release: 1.1.1-1.1.1
    :fls: fls_vjgkg8kfi93
    :decidability: decidable
    :scope: module
    :tags: stack-overflow

    Any function shall not call itself directly or indirectly

    .. rationale:: 
        :id: rat_S37NlKY0CMVx 
        :status: draft

        Recursive functions can easily cause stack overflows, which may result in exceptions or, in some cases, undefined behavior (typically some embedded systems). Although the Rust compiler supports `tail call optimization <https://en.wikipedia.org/wiki/Tail_call>`_\ , this optimization is not guaranteed and depends on the specific implementation and function structure. There is an `open RFC to guarantee tail call optimization in the Rust compiler <https://github.com/phi-go/rfcs/blob/guaranteed-tco/text/0000-explicit-tail-calls.md>`_\ , but this feature has not yet been stabilized. Until tail call optimization is guaranteed and stabilized, developers should avoid using recursive functions to prevent potential stack overflows and ensure program reliability.

    .. non_compliant_example::
        :id: non_compl_ex_BQ2jUEuSxKNo 
        :status: draft

        The below function concat_strings is not complaint because it call itself and depending on depth of data provided as input it could generate an stack overflow exception or undefine behavior.

        .. code-block:: rust

            // Recursive enum to represent a string or a list of `MyEnum`
              enum MyEnum {
                  Str(String),
                  List(Vec<MyEnum>),
              }

              // Concatenates strings from a nested structure of `MyEnum` using recursion.
              fn concat_strings(input: &[MyEnum]) -> String {
                  let mut result = String::new();
                  for item in input {
                      match item {
                          MyEnum::Str(s) => result.push_str(s),
                          MyEnum::List(list) => result.push_str(&concat_strings(list)),
                      }
                  }
                  result
              }

    .. compliant_example::
        :id: compl_ex_vVT4VZJOWssx 
        :status: draft

        tete

        .. code-block:: rust

            // Recursive enum to represent a string or a list of `MyEnum`
              enum MyEnum {
                  Str(String),
                  List(Vec<MyEnum>),
              }

              /// Concatenates strings from a nested structure of `MyEnum` without using recursion.
              /// Returns an error if the stack size exceeds `MAX_STACK_SIZE`.
              fn concat_strings_non_recursive(input: &[MyEnum]) -> Result<String, &'static str> {
                 const MAX_STACK_SIZE: usize = 1000;
                 let mut result = String::new();
                 let mut stack = Vec::new();

                 // Add all items to the stack
                 stack.extend(input.iter());

                 while let Some(item) = stack.pop() {
                      match item {
                          MyEnum::Str(s) => result.insert_str(0, s),
                          MyEnum::List(list) => {
                              // Add list items to the stack
                              for sub_item in list.iter() {
                                  stack.push(sub_item);
                                  if stack.len() > MAX_STACK_SIZE {
                                      return Err("Too big structure");
                                  }
                              }
                          }
                      }
                  }
                  Ok(result)
              }
