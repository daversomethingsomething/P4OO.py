'''
Perforce Object-Oriented Abstraction (P4OO)

P4OO provides a domain object modeled representation of Perforce.
It is designed to be easy to use, and to provide a natural OO
interface to Perforce.

Traditionally using P4Python, in order to get the last change
on a label you would do the following:

- `p4 changes -m 1 @labelFoo`

To accomplish the same with P4OO, we will do the following:

- `P4OOLabel(id="labelFoo").getLastChange().id`

Of course, it's rare that you are trying to do something that simple.
Usually you want to do something with that change, that's why you
were looking for it.

Perhaps you want to look at the list of changes between two labels
for the files in your client.

That looks something like this:

- Get Last change on first label
- Get Last change on the second label
- For each line in your client view spec
  - Get list of changes from first change to last change
- Return the union all detected changes

Part of the reason for this complexity is that Perforce is extremely
flexible in its view specs.  All of these queries are relative to the
files identified by your client's view spec.  Which is arbitrary, not
a guaranteed consistent view of the depot(s).

Everyone who has ever wanted to ask Perforce that question has had to
implement that algorithm.  Given the parsing and complexity involved,
that is a fairly error-prone venture.  Multiply that by every query
a release engineer has ever drempt up to build their release notes and
we end up with an unreasonable burden and a quality nightmare.

Using P4OO, we can codify such commonly used algorithms into an API
using our framework for interacting with Perforce Specs.

That particular query is provided by our Label object for instance:

- `P4OOLabel(id="labelFoo").getChangesFromLabels(P4OOLabel(id="labelBar"),
                                                           P4OOClient())`

Now, the kicker is that you are returned a P4OOChangeSet object
containing multiple P4OOChange objects.  You can then leverage
those P4OO objects within the framework to query more information
about them.  Description, user, jobs, etc.

In this example, you'll see some patterns that are used throughout
the P4OO framework.  Methods will generally return other P4OO
objects, when the answers involve other Perforce entities.   These
returned objects will reuse the same P4Python handle for subsequent
queries.

The "id" attribute is used consistently throughout P4OO to identify
unique P4OO Spec objects, and is set to the name of the spec used
within Perforce.

When constructing a P4OO Spec object, only "id" is required.  Once
the object is constructed, you can use the object to query Perforce
for the other object attributes, such as the creator/owner of a label:

    p4labelObj = P4OOLabel(id="P4-OO-0.00_01")
    p4LabelOwner = p4LabelObj._getSpecAttr("Owner")

'''
