# garberize

When a CSS file and an HTML (or markdown) file fall in love and get married, they make an HTML file with inlined CSS.

*This is a prototype; very much an experiment.* I don't know what the final form of this will take, but it appears that it will be useful for some projects.

## Run it

    $ garberize -c thestyle.css content.md > inlined.html

## Excuse it

Some thing garberize will not do:

* care about selector precedence, top to bottom is how we roll
* fancy stuff

## Example

content.md:

    # An important headline

    We've got a smattering of stuff.

    ## The first thing
    ### Has a subheading

    **Lorem ipsum dolor sit amet, consectetur adipisicing elit,** sed do eiusmod
    tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
    quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
    consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
    cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
    proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

style.css:

    h1, h2, h3, h4, h5 { font-family: sans-serif; }
    h2 { color: #D64; }
    h3 { color: #F96; }
    p { line-height: 140%; }

begat inlined.html:

    <html>
        <body>
            <h1 style="font-family: sans-serif;">This Week in Sunlight</h1>
            <p style="line-height: 140%;">We've got a smattering of mentions.</p>
            <h2 style="font-family: sans-serif; color: #D64;">Transparency Connect</h2>
            <h3 style="font-family: sans-serif; color: #F96;">Putting you in touch with Congress</h3>
            <p style="line-height: 140%;">
                <strong>Lorem ipsum dolor sit amet, consectetur adipisicing elit,</strong> sed do eiusmod
                tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
                quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
                consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
                cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
                proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            </p>
        </body>
    </html>
