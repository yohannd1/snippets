# To be used in game

import
  options, sugar

type
  GenerationID* = uint32

  IndexingPair* = object
    index*: uint
    gen*: uint32

  AlreadyFreedError* = object of CatchableError
  BadGenerationError* = object of CatchableError
    desired_gen*: GenerationID
    found_gen*: GenerationID

  GenMap*[T] = object
    current_gen: GenerationID
    data: seq[Option[GenEntry[T]]]

  GenEntry*[T] = object
    gen: GenerationID
    val*: T

# TODO: find a way to free up allocated space that has no entity

proc add[T](map: var GenMap[T], val: T): IndexingPair =
  var i: uint = 0
  while i < map.data.len().uint:
    if map.data[i].isNone():
      map.data[i] = some[GenEntry[T]](GenEntry[T](gen: map.current_gen, val: val))
      map.current_gen += 1
      return IndexingPair(index: i, gen: map.current_gen - 1)
    i += 1

  map.data.add some[GenEntry[T]](GenEntry[T](gen: map.current_gen, val: val))
  map.current_gen += 1
  return IndexingPair(index: map.data.len.uint - 1, gen: map.current_gen - 1)

proc removeAt[T](map: var GenMap[T], index: uint, gen: uint32) {.raises: [IndexDefect, AlreadyFreedError, BadGenerationError].} =
  let data = map.data[index]

  if data.isNone():
    raise AlreadyFreedError.new

  let found_gen = data.get().gen
  if found_gen != gen:
    raise (ref BadGenerationError)(desired_gen: gen, found_gen: found_gen)

  map.data[index] = none[GenEntry[T]]()

proc removeAtAnyGen[T](map: var GenMap[T], index: uint) {.raises: [IndexDefect, AlreadyFreedError].} =
  if map.data[index].isNone():
    raise AlreadyFreedError.new
  map.data[index] = none[GenEntry[T]]()

proc getAt[T](map: var GenMap[T], index: uint, gen: uint32): Option[T] {.raises: [IndexDefect].} =
  let data = map.data[index]
  if map.data[index].isNone():
    return none[T]()
  let dsome = data.get()
  if dsome.gen != gen:
    return none[T]()
  return some(dsome.val)

proc getAtAnyGen[T](map: var GenMap[T], index: uint): Option[T] {.raises: [IndexDefect].} =
  map.data[index].map(inner => inner.val)

var map = GenMap[int8]()
discard map.add 20
discard map.add 50
map.removeAtAnyGen(0)
discard map.add 16
echo map.getAtAnyGen(0)
