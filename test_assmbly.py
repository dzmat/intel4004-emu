import unittest

from executor import Executor
import translator


class TestASM(unittest.TestCase):

    @staticmethod
    def run_assembly(src, inp=None):
        prg = translator.translate(src.splitlines())
        cpu = Executor()
        if inp:
            cpu.regs = [int(x, 16) for x in inp.split()]
        cpu.run(prg)
        return ' '.join('{:x}'.format(x) for x in cpu.regs)

    def test_wiki_examples(self):
        asm = '''\
ldm 5
xch r2'''
        self.assertEqual('0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0', self.run_assembly(asm))

        asm = '''\
start:
  iac
  xch r1
finish:
  nop
'''
        self.assertEqual('0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0', self.run_assembly(asm))

        asm = '''\
fim r0 $31
fim r2 $41
fim r4 $59
fim r6 $26
fim r12 250
fim r14 206
'''
        self.assertEqual('3 1 4 1 5 9 2 6 0 0 0 0 f a c e', self.run_assembly(asm))

        asm = '''\
ldm 6
ral
xch r0

ldm 8
rar
xch r1

ldm 7
rar
rar
xch r2
'''
        self.assertEqual('c 4 9 0 0 0 0 0 0 0 0 0 0 0 0 0', self.run_assembly(asm))

        asm = '''\
ldm 5
xch r0
jun skip_few
ldm 6
xch r1
skip_few:
ldm 7
xch r2
'''
        self.assertEqual('5 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0', self.run_assembly(asm))

        asm = '''\
ldm 0
xch r0

jms add_three
jms add_three
jms add_three
jun finish

add_three:
ld r0
iac
iac
iac
xch r0
bbl 0

finish:
nop
'''
        self.assertEqual('9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0', self.run_assembly(asm))


if __name__ == '__main__':
    unittest.main()