# Copyright 2023 Sofia
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

def split_with_quotes(s: str, sep: str = " ", quote: str = '"') -> list[str]:
    """
    Splits the string on each space but keeps stuff inside double quotes the same.

    No, no handling for backslashes right now. I've kind of jury rigged the quote checking
    when string slicing so it might be kinda icky to implement (probably).
    """
    assert len(sep) == 1, "Separator must be a single character"
    assert len(quote) == 1, "Symbol for quote must be a single character"

    # Remove separators from the edges of the string, this can cause problems later
    # that i don't want to deal with
    s = s.strip(sep)

    # What'll be returned
    result = list()
    
    # An empty string will cause idx to never be set which causes an UnboundLocalError exception
    if s == "":
        return result
    
    # For tracking whether we are inside quotes or not
    in_quotes = False
    
    # For tracking where to slice the string
    start_idx = 0
    end_idx = -1
    
    for idx in range(len(s)):
        # Change quote mode
        if s[idx] == quote:
            in_quotes = not in_quotes

        if (in_quotes and s[idx] == quote) or (not in_quotes and s[idx] == sep):
            # Oh! This is a separator!

            # We dont want to add empty strings
            # This happens when there are two separators in a row or some
            # weird thing with the quotes
            if start_idx >= idx:
                # Skip the extra separator
                start_idx += 1

                # Try again
                continue
            
            # At the end of a quote we need to skip the ending quote character
            del_quote = 1 if s[idx - 1] == quote else 0
            result.append(s[start_idx: idx - del_quote])

            # +1 to skip the separator
            start_idx = idx + 1 

            # Remember the last idx of what was sliced            
            end_idx = idx
        
    # This means there was an unclosed quote
    if in_quotes:
        raise SyntaxError("Unclosed quotation")

    # Check if the last portion was added
    if end_idx < idx:
        # no need to check for seps at the end bc they got stripped
        
        # So if the last one does not have any quotes,,, just add it
        if s[-1] != quote:
            result.append(s[start_idx:])
        
        # But if it does have quotes! Skip em!
        else:
            result.append(s[start_idx: -1])
    
    return result
