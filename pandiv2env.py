#!/usr/bin/env python

import panflute

def div2env(elem, doc, debug=False):
    if type(elem) == panflute.Div and doc.format in ["latex", "beamer"]:
        attr = getattr(elem, "attributes", None)
        if not attr:
            return

        env = attr.get("data-environment", "").split(",")
        if not env[0]:
            # This is not marked as an environment
            return

        # Convert the positional arguments to the proper \LaTeX format
        args = attr.get("data-environment-args", "").split("|")
        args = "{{{0}}}".format("}{".join(args)) + "{}" if args[0] else "{}{}"

        # Enclose the keyword arguments in '[...]'
        opt = attr.get("data-environment-keyword", "")
        opt = "[{0}]".format(opt) if opt else ""

        begin = panflute.RawInline(
                "\\begin{{{0}}}{1}{2}%\n".format(env[0], opt, args),
                format="latex"
            )
        end = panflute.RawInline(
                "%\n\\end{{{0}}}".format(env[0]),
                format="latex"
            )
        if debug:
            panflute.debug("begin = '{0!s}'".format(begin))
            panflute.debug("end = '{0!s}'".format(end))

        # Check if the first content item is a list
        if isinstance(elem.content[0], panflute.ListItem):
            # Directly prepend and append the begin and end environments to the list
            elem.content[0].content.insert(0, begin)
            elem.content[0].content.append(end)
        else:
            # For non-list items, wrap them in Para elements as before
            elem.content.insert(0, panflute.Para(begin))
            elem.content.append(panflute.Para(end))

        if debug:
            panflute.debug("content = '{0!s}'".format(elem.content))

        return elem

    return

def main(doc=None):
    return panflute.run_filter(div2env, doc=doc)

if __name__ == "__main__":
    main()
