class RecursiveCharacterSplitter:

    def __init__(
        self,
        chunk_size=800,
        chunk_overlap=100,
        separators=None
    ):

        self.chunk_size = chunk_size

        self.chunk_overlap = chunk_overlap

        self.separators = separators or [
            "\n\n",
            "\n",
            " ",
            ""
        ]

    def split_text(self, text: str) -> list[str]:

        return self._split_text(
            text,
            self.separators
        )

    def _split_text(
        self,
        text: str,
        separators: list[str]
    ) -> list[str]:

        final_chunks = []

        # Find the first separator present in the text
        separator = separators[-1]

        new_separators = []

        for i, s in enumerate(separators):

            if s == "":

                separator = s

                break

            if s in text:

                separator = s

                new_separators = separators[
                    i + 1:
                ]

                break

        # Split text by separator
        if separator != "":

            splits = text.split(separator)

        else:

            splits = list(text)

        good_splits = [
            s
            for s in splits
            if s.strip() or s == "\n"
        ]

        current_doc = []

        total = 0

        for s in good_splits:

            d_len = len(s)

            sep_len = len(separator) if current_doc else 0

            if total + d_len + sep_len <= self.chunk_size:

                current_doc.append(s)

                total += d_len + sep_len

            else:

                if current_doc:

                    joined = separator.join(
                        current_doc
                    )

                    final_chunks.append(joined)

                    # Compute overlap
                    overlap_doc = []

                    overlap_total = 0

                    for os in reversed(
                        current_doc
                    ):

                        os_len = len(os)

                        o_sep_len = len(separator) if overlap_doc else 0

                        if overlap_total + os_len + o_sep_len <= self.chunk_overlap:

                            overlap_doc.insert(
                                0,
                                os
                            )

                            overlap_total += os_len + o_sep_len

                        else:

                            break

                    current_doc = overlap_doc

                    total = overlap_total

                if d_len > self.chunk_size:

                    if new_separators:

                        recursive_chunks = self._split_text(
                            s,
                            new_separators
                        )

                        final_chunks.extend(
                            recursive_chunks
                        )

                    else:

                        for j in range(
                            0,
                            d_len,
                            self.chunk_size
                        ):

                            final_chunks.append(
                                s[
                                    j:j + self.chunk_size
                                ]
                            )

                else:

                    current_doc.append(s)

                    total += d_len

        if current_doc:

            final_chunks.append(
                separator.join(current_doc)
            )

        return final_chunks


text_splitter = RecursiveCharacterSplitter(
    chunk_size=800,
    chunk_overlap=100
)


def split_text(text):

    if not text:
        return []

    return text_splitter.split_text(text)