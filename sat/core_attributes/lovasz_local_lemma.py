import numpy as np
from sat.instance.instance import Instance


def is_lll_satisfied(instance: Instance) -> bool:
    """
    Check whether given instance can be unsatisfiable.
    "Lovasz-Local-Lemma".

    Meine Erklärung für das LLL:
    Damit eine Formel überhaupt unerfüllbar sein kann,
    muss für jede Klausel folgende Überlegung gelten:
        Damit JEDE Belegung, die diese Klausel erfüllen würde,
        die ganze Formel F im Endeffekt nicht erfüllt (Fall: F unerfüllbar),
        muss es GENUG andere Klauseln geben, die genau dafür sorgen.

        Bsp: Enthält eine Klausel nur 3 Variablen (a,b,c | Angenommen es gibt insg. nur a,b,c,d),
        so schießt der Biathlet zwei Scheiben ab.
        Wenn F unerfüllbar ist, so werden alle Scheiben abgeschossen.
        Dafür müssen alle Scheiben mit allen anderen Kombis von a,b,c-literalen abgeschossen werden.
        Dafür braucht es Schüsse, die auf sie zielen.
        Das sind eben Klauseln, die diese Variablen enthalten.

    :param instance:
    :return:
        true <--> core-instance,
        false <--> trivially satisfiable (due to lll)
    """

    bit_matrix = instance.get_bit_matrix()

    k = np.sum(bit_matrix[0])
    for clause in bit_matrix:
        if np.sum(clause) != k:
            raise Exception(
                "LLL not applicable, because not every clause has same length k"
            )

    var_occs = np.zeros((bit_matrix.shape[0], bit_matrix.shape[1] // 2), dtype=np.uint8)
    for i in range(var_occs.shape[0]):
        for j in range(var_occs.shape[1]):
            var_occs[i, j] = bit_matrix[i, 2 * j] or bit_matrix[i, 2 * j + 1]

    for i in range(instance.num_clauses):

        associated_counter = 0
        for j in range(instance.num_clauses):

            if i == j:
                continue

            if 2 in (var_occs[i] + var_occs[j]):
                associated_counter += 1

        if associated_counter >= 2 ** (k - 2):
            return True

    return False
