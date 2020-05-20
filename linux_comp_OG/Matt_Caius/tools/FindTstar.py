def Find_Tstar(TPMlist,referenceTPM,type = -np.inf):

    norms = list()

    for TPM in TPMlist:

        difference = referenceTPM - TPM
        norm = np.linalg.norm(difference,ord = type)
        norms.append(norm)

    print(norms)
    index = 0

    for norm in norms:

        if norm == np.min(norms):
            break
        index += 1

    return index